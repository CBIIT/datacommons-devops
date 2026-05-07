import aws_cdk as cdk
from aws_cdk.assertions import Template, Match

from configparser import ConfigParser

from app import build_stack


def _create_test_stack():
    """Helper function to create a test stack with consistent configuration.

    Stack creation steps are sourced from app/__init__.py (build_stack) to
    keep the test in sync with the real deployment entrypoint (app.py).
    The synthesizer is omitted here — it is only needed for CDK bootstrap
    role resolution during actual deployments.
    """
    outdir = "tests/cdk.out"
    app = cdk.App(outdir=str(outdir))

    config = ConfigParser(interpolation=None)
    config.read('config.ini')

    stack = build_stack(app, config)

    return stack, Template.from_stack(stack), config


def test_opensearch_encryption():
    """Test OpenSearch domain has encryption enabled if deployed"""
    stack, template, config = _create_test_stack()

    # Only test if OpenSearch is deployed
    opensearch_resources = template.find_resources("AWS::OpenSearchService::Domain")
    if not opensearch_resources:
        return

    template.has_resource_properties("AWS::OpenSearchService::Domain", {
        "NodeToNodeEncryptionOptions": {
            "Enabled": True
        },
        "EncryptionAtRestOptions": {
            "Enabled": True
        },
        "DomainEndpointOptions": {
            "EnforceHTTPS": True
        }
    })


def test_opensearch_access_policies():
    """Test that the OpenSearch security group permits port 443 access from the backend service security group"""
    stack, template, config = _create_test_stack()

    # Only test if OpenSearch is deployed
    opensearch_resources = template.find_resources("AWS::OpenSearchService::Domain")
    if not opensearch_resources:
        return

    # Extract the security group logical IDs assigned to the OpenSearch domain from VPCOptions
    # CDK renders SecurityGroupIds as Fn::GetAtt references (not Ref)
    os_sg_refs = []
    for _, resource in opensearch_resources.items():
        vpc_opts = resource.get("Properties", {}).get("VPCOptions", {})
        for sg_id in vpc_opts.get("SecurityGroupIds", []):
            if "Fn::GetAtt" in sg_id:
                os_sg_refs.append(sg_id["Fn::GetAtt"][0])
            elif "Ref" in sg_id:
                os_sg_refs.append(sg_id["Ref"])

    assert os_sg_refs, "OpenSearch domain should have at least one VPC security group assigned"

    # Find SecurityGroupIngress rules that specifically target the OpenSearch security group(s)
    # CDK emits GroupId as Fn::GetAtt referencing the SG logical ID (not Ref)
    ingress_resources = template.find_resources("AWS::EC2::SecurityGroupIngress")

    def _sg_logical_id(ref):
        if "Fn::GetAtt" in ref:
            return ref["Fn::GetAtt"][0]
        if "Ref" in ref:
            return ref["Ref"]
        return None

    os_ingress_rules = [
        rule for rule in ingress_resources.values()
        if _sg_logical_id(rule.get("Properties", {}).get("GroupId", {})) in os_sg_refs
    ]
    assert len(os_ingress_rules) > 0, "Expected at least one ingress rule targeting the OpenSearch security group"

    # At least one rule must allow port 443 access from a service security group
    sg_source_rules = [
        rule for rule in os_ingress_rules
        if rule.get("Properties", {}).get("FromPort") == 443
        and "SourceSecurityGroupId" in rule.get("Properties", {})
    ]
    assert len(sg_source_rules) > 0, "Expected at least one port 443 ingress rule on the OpenSearch security group sourced from a service security group"


def test_opensearch_vpc_security():
    """Test OpenSearch is secured within VPC with proper subnet configuration if deployed"""
    stack, template, config = _create_test_stack()

    # Only test if OpenSearch is deployed
    opensearch_resources = template.find_resources("AWS::OpenSearchService::Domain")
    if not opensearch_resources:
        return

    template.has_resource_properties("AWS::OpenSearchService::Domain", {
        "VPCOptions": {
            "SubnetIds": Match.any_value(),
            "SecurityGroupIds": Match.any_value()
        }
    })


def test_opensearch_single_az_security():
    """Test OpenSearch is configured for single AZ if deployed (security requirement)"""
    stack, template, config = _create_test_stack()

    # Only test if OpenSearch is deployed
    opensearch_resources = template.find_resources("AWS::OpenSearchService::Domain")
    if not opensearch_resources:
        return

    template.has_resource_properties("AWS::OpenSearchService::Domain", {
        "ClusterConfig": {
            "MultiAZWithStandbyEnabled": False,
            "ZoneAwarenessEnabled": False
        }
    })


def test_iam_role_naming_aspect():
    """Test that MyAspect correctly applies role naming for security compliance"""
    stack, template, config = _create_test_stack()

    # Roles should have the prefix applied by MyAspect for compliance
    expected_prefix = f"{config['iam']['role_prefix']}-{config['main']['tier']}"
    
    template.has_resource_properties("AWS::IAM::Role", {
        "RoleName": Match.string_like_regexp(f"^{expected_prefix}-.*")
    })


def test_permission_boundaries():
    """Test that permission boundaries are applied to IAM roles for security compliance"""
    stack, template, config = _create_test_stack()

    if config.has_option('iam', 'permission_boundary'):
        template.has_resource_properties("AWS::IAM::Role", {
            "PermissionsBoundary": config['iam']['permission_boundary']
        })


def test_iam_role_trust_policies():
    """Test that IAM roles have appropriate trust policies"""
    stack, template, config = _create_test_stack()

    # ECS task roles should trust ECS tasks service
    template.has_resource_properties("AWS::IAM::Role", {
        "AssumeRolePolicyDocument": {
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ecs-tasks.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
    })


def test_container_secrets_security():
    """Test that containers retrieve secrets securely from Secrets Manager if deployed"""
    stack, template, config = _create_test_stack()

    # Only test if task definitions with secrets are deployed
    task_def_resources = template.find_resources("AWS::ECS::TaskDefinition")
    if not task_def_resources:
        return

    # Containers should get secrets from Secrets Manager, not environment variables
    # Secrets use Fn::Join with secret reference and field name
    template.has_resource_properties("AWS::ECS::TaskDefinition", {
        "ContainerDefinitions": [
            {
                "Secrets": Match.array_with([
                    {
                        "Name": Match.any_value(),
                        "ValueFrom": {
                            "Fn::Join": Match.any_value()  # Validates Fn::Join structure exists
                        }
                    }
                ])
            }
        ]
    })


def test_alb_https_enforcement():
    """Test that ALB enforces HTTPS by redirecting HTTP traffic if deployed"""
    stack, template, config = _create_test_stack()

    # Only test if an ALB is deployed
    if not template.find_resources("AWS::ElasticLoadBalancingV2::LoadBalancer"):
        return

    # HTTP listener (port 80) should redirect to HTTPS
    template.has_resource_properties("AWS::ElasticLoadBalancingV2::Listener", {
        "Port": 80,
        "Protocol": "HTTP",
        "DefaultActions": [
            {
                "Type": "redirect",
                "RedirectConfig": {
                    "Protocol": "HTTPS",
                    "Port": "443",
                    "StatusCode": "HTTP_301"
                }
            }
        ]
    })


def test_alb_ssl_certificate():
    """Test that ALB uses SSL certificate for HTTPS if deployed"""
    stack, template, config = _create_test_stack()

    # Only test if an ALB is deployed
    if not template.find_resources("AWS::ElasticLoadBalancingV2::LoadBalancer"):
        return

    # HTTPS listener should have valid certificate
    template.has_resource_properties("AWS::ElasticLoadBalancingV2::Listener", {
        "Port": 443,
        "Protocol": "HTTPS",
        "Certificates": [
            {
                "CertificateArn": config["alb"]["certificate_arn"]
            }
        ]
    })


def test_alb_security_policy():
    """Test that ALB uses secure SSL security policy if deployed"""
    stack, template, config = _create_test_stack()

    # Only test if an ALB is deployed
    if not template.find_resources("AWS::ElasticLoadBalancingV2::LoadBalancer"):
        return

    # HTTPS listener should use a secure SSL policy
    template.has_resource_properties("AWS::ElasticLoadBalancingV2::Listener", {
        "Port": 443,
        "Protocol": "HTTPS",
        "SslPolicy": "ELBSecurityPolicy-TLS13-1-2-2021-06"  # Secure SSL policy that supports TLS 1.2 and 1.3"
    })


def test_network_isolation():
    """Test that ECS services are properly isolated in private subnets if deployed"""
    stack, template, config = _create_test_stack()

    # Only test if ECS services are deployed
    if not template.find_resources("AWS::ECS::Service"):
        return

    # ECS services should be in private subnets with no public IP
    template.has_resource_properties("AWS::ECS::Service", {
        "NetworkConfiguration": {
            "AwsvpcConfiguration": {
                "AssignPublicIp": "DISABLED",
                "Subnets": Match.any_value(),
                "SecurityGroups": Match.any_value()
            }
        }
    })


def test_cloudfront_key_security():
    """Test that CloudFront uses key-based security for signed URLs if deployed"""
    stack, template, config = _create_test_stack()

    # Only test if CloudFront key group is deployed
    keygroup_resources = template.find_resources("AWS::CloudFront::KeyGroup")
    if not keygroup_resources:
        return

    # CloudFront should have a key group for signed URLs
    template.has_resource_properties("AWS::CloudFront::KeyGroup", {
        "KeyGroupConfig": {
            "Items": Match.any_value(),
            "Name": Match.any_value()
        }
    })

    # CloudFront should have a public key
    template.has_resource_properties("AWS::CloudFront::PublicKey", {
        "PublicKeyConfig": {
            "Name": Match.any_value(),
            "EncodedKey": Match.any_value()
        }
    })


# def test_ec2_key_pair_security():
#     """Test that EC2 key pair is properly managed for CloudFront"""
#     stack, template, config = _create_test_stack()

#     expected_key_name = f"{config['main']['program']}-{config['main']['project']}-{config['main']['tier']}-cloudfront-key-pair"
    
#     template.has_resource_properties("AWS::EC2::KeyPair", {
#         "KeyName": expected_key_name,
#         "KeyType": "rsa"  # Secure key type
#     })


def test_opensearch_allowed_ips_security():
    """Test that the OpenSearch security group only permits port 443 ingress from authorized sources"""
    stack, template, config = _create_test_stack()

    # Only test if OpenSearch is deployed
    opensearch_resources = template.find_resources("AWS::OpenSearchService::Domain")
    if not opensearch_resources:
        return

    # Extract the security group logical IDs assigned to the OpenSearch domain
    # CDK renders SecurityGroupIds as Fn::GetAtt references (not Ref)
    os_sg_refs = []
    for _, resource in opensearch_resources.items():
        vpc_opts = resource.get("Properties", {}).get("VPCOptions", {})
        for sg_id in vpc_opts.get("SecurityGroupIds", []):
            if "Fn::GetAtt" in sg_id:
                os_sg_refs.append(sg_id["Fn::GetAtt"][0])
            elif "Ref" in sg_id:
                os_sg_refs.append(sg_id["Ref"])

    if not os_sg_refs:
        return

    # Find SecurityGroupIngress rules that specifically target the OpenSearch security group(s)
    # CDK emits GroupId as Fn::GetAtt referencing the SG logical ID (not Ref)
    def _sg_logical_id(ref):
        if "Fn::GetAtt" in ref:
            return ref["Fn::GetAtt"][0]
        if "Ref" in ref:
            return ref["Ref"]
        return None

    ingress_resources = template.find_resources("AWS::EC2::SecurityGroupIngress")
    os_ingress_rules = {
        rule_id: rule for rule_id, rule in ingress_resources.items()
        if _sg_logical_id(rule.get("Properties", {}).get("GroupId", {})) in os_sg_refs
    }

    # Every ingress rule targeting OpenSearch must use port 443 only
    # and must identify a specific authorized source (security group or CIDR — not open to the world)
    for rule_id, rule in os_ingress_rules.items():
        properties = rule.get("Properties", {})
        assert properties.get("FromPort") == 443, \
            f"Rule {rule_id}: OpenSearch only permits port 443 ingress, found port {properties.get('FromPort')}"
        assert properties.get("ToPort") == 443, \
            f"Rule {rule_id}: OpenSearch only permits port 443 ingress, found ToPort {properties.get('ToPort')}"
        has_sg_source = "SourceSecurityGroupId" in properties
        has_cidr_source = "CidrIp" in properties or "CidrIpv6" in properties
        assert has_sg_source or has_cidr_source, \
            f"Rule {rule_id}: OpenSearch ingress rule must identify a specific source (security group or CIDR)"


def test_task_role_permissions():
    """Test that ECS task roles have IAM inline policies and managed policy ARNs attached"""
    stack, template, config = _create_test_stack()

    # Task roles should have inline policies attached
    template.has_resource("AWS::IAM::Policy", {})

    # Roles should have managed policies attached (e.g. ECS execution role managed policies)
    template.has_resource_properties("AWS::IAM::Role", {
        "ManagedPolicyArns": Match.any_value()
    })


def test_log_group_retention():
    """Test that CloudWatch log groups enforce the required retention period if deployed"""
    stack, template, config = _create_test_stack()

    # Only test if log groups are explicitly deployed
    if not template.find_resources("AWS::Logs::LogGroup"):
        return

    # All log groups must enforce a 30-day retention period per security requirements
    template.has_resource_properties("AWS::Logs::LogGroup", {
        "RetentionInDays": 30
    })


def test_s3_bucket_security():
    """Test that ALB access logging to S3 is enabled if an ALB is deployed"""
    stack, template, config = _create_test_stack()

    # Only test if an ALB is deployed
    # No new S3 buckets are created by this stack; validates the ALB references an existing bucket securely
    if not template.find_resources("AWS::ElasticLoadBalancingV2::LoadBalancer"):
        return

    # ALB should log to a secure S3 bucket
    template.has_resource_properties("AWS::ElasticLoadBalancingV2::LoadBalancer", {
        "LoadBalancerAttributes": Match.array_with([
            {
                "Key": "access_logs.s3.enabled",
                "Value": "true"
            }
        ])
    })


def test_container_security_context():
    """Test that containers run with appropriate security settings if deployed"""
    stack, template, config = _create_test_stack()

    # Only test if ECS task definitions are deployed
    if not template.find_resources("AWS::ECS::TaskDefinition"):
        return

    # Containers should not run as privileged
    template.has_resource_properties("AWS::ECS::TaskDefinition", {
        "ContainerDefinitions": [
            {
                "Privileged": Match.absent(),  # Should not be privileged
                # "ReadonlyRootFilesystem": Match.any_value(),
                # "User": Match.any_value()
            }
        ]
    })


def test_fargate_security():
    """Test that Fargate is used for container security if task definitions are deployed"""
    stack, template, config = _create_test_stack()

    # Only test if ECS task definitions are deployed
    if not template.find_resources("AWS::ECS::TaskDefinition"):
        return

    # Tasks should require Fargate for better security isolation
    template.has_resource_properties("AWS::ECS::TaskDefinition", {
        "RequiresCompatibilities": ["FARGATE"],
        "NetworkMode": "awsvpc"  # Required for Fargate and provides better network isolation
    })


def test_ecs_container_insights():
    """Test that ECS cluster has Container Insights enabled if deployed"""
    stack, template, config = _create_test_stack()

    # Only test if an ECS cluster is deployed
    if not template.find_resources("AWS::ECS::Cluster"):
        return

    # Security rules require: Enable Container Insights on ECS clusters
    template.has_resource_properties("AWS::ECS::Cluster", {
        "ClusterSettings": [
            {
                "Name": "containerInsights",
                "Value": "enabled"
            }
        ]
    })


def test_alb_access_log_prefix():
    """Test that ALB access logs use the correct S3 prefix format if an ALB is deployed"""
    stack, template, config = _create_test_stack()

    # Only test if an ALB is deployed
    if not template.find_resources("AWS::ElasticLoadBalancingV2::LoadBalancer"):
        return

    # Security rules specify deterministic prefix: "{{program}}/{{tier}}/{{project}}/alb-access-logs"
    expected_prefix = f"{config['main']['program']}/{config['main']['tier']}/{config['main']['project']}/alb-access-logs"
    
    template.has_resource_properties("AWS::ElasticLoadBalancingV2::LoadBalancer", {
        "LoadBalancerAttributes": Match.array_with([
            {
                "Key": "access_logs.s3.enabled",
                "Value": "true"
            },
            {
                "Key": "access_logs.s3.prefix",
                "Value": expected_prefix
            }
        ])
    })


def test_opensearch_slow_logging():
    """Test that OpenSearch has slow logs enabled to CloudWatch as per security rules"""
    stack, template, config = _create_test_stack()

    # Only test if OpenSearch is deployed
    opensearch_resources = template.find_resources("AWS::OpenSearchService::Domain")
    if not opensearch_resources:
        return

    # Security rules require: enable slow logs to CloudWatch Logs with dedicated log groups
    template.has_resource_properties("AWS::OpenSearchService::Domain", {
        "LogPublishingOptions": {
            "SEARCH_SLOW_LOGS": {
                "CloudWatchLogsLogGroupArn": Match.any_value(),
                "Enabled": True
            },
            "INDEX_SLOW_LOGS": {
                "CloudWatchLogsLogGroupArn": Match.any_value(),
                "Enabled": True
            }
        }
    })


def test_removal_policies():
    """Test that removal policies default to DESTROY as per security rules"""
    stack, template, config = _create_test_stack()

    # Security rules specify: Default to RemovalPolicy.Destroy for resources created by the stack
    # Test key resources have DeletionPolicy: Delete (CloudFormation equivalent of RemovalPolicy.DESTROY)
    
    # OpenSearch domain should have DESTROY removal policy
    opensearch_resources = template.find_resources("AWS::OpenSearchService::Domain")
    for resource_id, resource in opensearch_resources.items():
        assert resource.get("DeletionPolicy") == "Delete", f"OpenSearch domain {resource_id} should have DeletionPolicy: Delete"

    # Log groups should have DESTROY removal policy  
    log_group_resources = template.find_resources("AWS::Logs::LogGroup")
    for resource_id, resource in log_group_resources.items():
        assert resource.get("DeletionPolicy") == "Delete", f"Log group {resource_id} should have DeletionPolicy: Delete"


def test_cloudfront_https_enforcement():
    """Test that the CloudFront distribution enforces HTTPS via redirect on the default behavior if deployed"""
    stack, template, config = _create_test_stack()

    # Only test if a CloudFront distribution is deployed
    if not template.find_resources("AWS::CloudFront::Distribution"):
        return

    # viewer_protocol_policy=REDIRECT_TO_HTTPS is set on the default behavior in stack.py
    # CloudFormation renders this as ViewerProtocolPolicy: redirect-to-https
    template.has_resource_properties("AWS::CloudFront::Distribution", {
        "DistributionConfig": {
            "DefaultCacheBehavior": {
                "ViewerProtocolPolicy": "redirect-to-https"
            }
        }
    })


def test_cloudfront_distribution_uses_key_group():
    """Test that the CloudFront distribution enforces signed URLs via a trusted key group if deployed"""
    stack, template, config = _create_test_stack()

    # Only test if a CloudFront distribution is deployed
    if not template.find_resources("AWS::CloudFront::Distribution"):
        return

    # trusted_key_groups=[key_group] is set on the default behavior in stack.py
    # CloudFormation renders this as TrustedKeyGroups in DefaultCacheBehavior
    # This ensures unsigned requests are rejected by the distribution
    template.has_resource_properties("AWS::CloudFront::Distribution", {
        "DistributionConfig": {
            "DefaultCacheBehavior": {
                "TrustedKeyGroups": Match.any_value()
            }
        }
    })


def test_no_public_ingress_to_services():
    """Test that only the ALB accepts inbound traffic from the public internet (ports 80 and 443)"""
    stack, template, config = _create_test_stack()

    # The ALB is internet-facing (open=True on both port 80 and 443 listeners), so 0.0.0.0/0
    # ingress on those ports is expected. No other resource should accept public internet ingress.
    ingress_resources = template.find_resources("AWS::EC2::SecurityGroupIngress")
    open_rules = [
        (rule_id, rule) for rule_id, rule in ingress_resources.items()
        if "0.0.0.0/0" in rule.get("Properties", {}).get("CidrIp", "")
        or "::/0" in rule.get("Properties", {}).get("CidrIpv6", "")
    ]

    for rule_id, rule in open_rules:
        properties = rule.get("Properties", {})
        from_port = properties.get("FromPort")
        to_port = properties.get("ToPort")
        assert from_port in [80, 443] and to_port in [80, 443], (
            f"Rule {rule_id}: public internet ingress (0.0.0.0/0) is only permitted on ALB ports "
            f"80 and 443, but found FromPort={from_port} ToPort={to_port}"
        )


if __name__ == "__main__":
    # Run all security tests, exclude test_cloudfront_distribution_uses_key_group
    security_test_functions = [
        test_opensearch_encryption,
        test_opensearch_access_policies,
        test_opensearch_vpc_security,
        test_opensearch_single_az_security,
        test_iam_role_naming_aspect,
        test_permission_boundaries,
        test_iam_role_trust_policies,
        test_container_secrets_security,
        test_alb_https_enforcement,
        test_alb_ssl_certificate,
        test_alb_security_policy,
        test_network_isolation,
        test_cloudfront_key_security,
        test_opensearch_allowed_ips_security,
        test_task_role_permissions,
        test_log_group_retention,
        test_s3_bucket_security,
        test_container_security_context,
        test_fargate_security,
        test_ecs_container_insights,
        test_alb_access_log_prefix,
        test_opensearch_slow_logging,
        test_removal_policies,
        test_cloudfront_https_enforcement,
        test_no_public_ingress_to_services,
    ]
    
    print("Running comprehensive CDK Security tests...")
    failed_tests = []
    
    for test_func in security_test_functions:
        try:
            test_func()
            print(f"✅ {test_func.__name__}")
        except Exception as e:
            print(f"❌ {test_func.__name__}: {str(e)}")
            failed_tests.append(test_func.__name__)
    
    if failed_tests:
        print(f"\n{len(failed_tests)} security tests failed:")
        for test in failed_tests:
            print(f"  - {test}")
    else:
        print(f"\nAll {len(security_test_functions)} CDK Security tests passed successfully!")
