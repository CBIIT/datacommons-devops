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

    opensearch_resources = template.find_resources("AWS::OpenSearchService::Domain")
    if not opensearch_resources:
        return

    os_sg_refs = []
    for _, resource in opensearch_resources.items():
        vpc_opts = resource.get("Properties", {}).get("VPCOptions", {})
        for sg_id in vpc_opts.get("SecurityGroupIds", []):
            if "Fn::GetAtt" in sg_id:
                os_sg_refs.append(sg_id["Fn::GetAtt"][0])
            elif "Ref" in sg_id:
                os_sg_refs.append(sg_id["Ref"])

    assert os_sg_refs, "OpenSearch domain should have at least one VPC security group assigned"

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

    sg_source_rules = [
        rule for rule in os_ingress_rules
        if rule.get("Properties", {}).get("FromPort") == 443
        and "SourceSecurityGroupId" in rule.get("Properties", {})
    ]

    assert len(sg_source_rules) > 0, "Expected at least one port 443 ingress rule on the OpenSearch security group sourced from a service security group"


def test_opensearch_vpc_security():
    """Test OpenSearch is secured within VPC with proper subnet configuration if deployed"""
    stack, template, config = _create_test_stack()

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

    task_def_resources = template.find_resources("AWS::ECS::TaskDefinition")
    if not task_def_resources:
        return

    template.has_resource_properties("AWS::ECS::TaskDefinition", {
        "ContainerDefinitions": [
            {
                "Secrets": Match.array_with([
                    {
                        "Name": Match.any_value(),
                        "ValueFrom": {
                            "Fn::Join": Match.any_value()
                        }
                    }
                ])
            }
        ]
    })


def test_alb_https_enforcement():
    """Test that ALB enforces HTTPS by redirecting HTTP traffic if deployed"""
    stack, template, config = _create_test_stack()

    if not template.find_resources("AWS::ElasticLoadBalancingV2::LoadBalancer"):
        return

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

    if not template.find_resources("AWS::ElasticLoadBalancingV2::LoadBalancer"):
        return

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

    if not template.find_resources("AWS::ElasticLoadBalancingV2::LoadBalancer"):
        return

    template.has_resource_properties("AWS::ElasticLoadBalancingV2::Listener", {
        "Port": 443,
        "Protocol": "HTTPS",
        "SslPolicy": "ELBSecurityPolicy-TLS13-1-2-2021-06"
    })


def test_network_isolation():
    """Test that ECS services are properly isolated in private subnets if deployed"""
    stack, template, config = _create_test_stack()

    if not template.find_resources("AWS::ECS::Service"):
        return

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

    keygroup_resources = template.find_resources("AWS::CloudFront::KeyGroup")
    if not keygroup_resources:
        return

    template.has_resource_properties("AWS::CloudFront::KeyGroup", {
        "KeyGroupConfig": {
            "Items": Match.any_value(),
            "Name": Match.any_value()
        }
    })

    template.has_resource_properties("AWS::CloudFront::PublicKey", {
        "PublicKeyConfig": {
            "Name": Match.any_value(),
            "EncodedKey": Match.any_value()
        }
    })


def test_opensearch_allowed_ips_security():
    """Test that the OpenSearch security group only permits port 443 ingress from authorized sources"""
    stack, template, config = _create_test_stack()

    opensearch_resources = template.find_resources("AWS::OpenSearchService::Domain")
    if not opensearch_resources:
        return

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

    for rule_id, rule in os_ingress_rules.items():
        properties = rule.get("Properties", {})
        assert properties.get("FromPort") == 443
        assert properties.get("ToPort") == 443

        has_sg_source = "SourceSecurityGroupId" in properties
        has_cidr_source = "CidrIp" in properties or "CidrIpv6" in properties

        assert has_sg_source or has_cidr_source


def test_task_role_permissions():
    """Test that ECS task roles have IAM inline policies and managed policy ARNs attached"""
    stack, template, config = _create_test_stack()

    template.has_resource("AWS::IAM::Policy", {})

    template.has_resource_properties("AWS::IAM::Role", {
        "ManagedPolicyArns": Match.any_value()
    })


def test_log_group_retention():
    """Test that CloudWatch log groups enforce the required retention period if deployed"""
    stack, template, config = _create_test_stack()

    if not template.find_resources("AWS::Logs::LogGroup"):
        return

    template.has_resource_properties("AWS::Logs::LogGroup", {
        "RetentionInDays": 30
    })


def test_s3_bucket_security():
    """Test that ALB access logging to S3 is enabled if an ALB is deployed"""
    stack, template, config = _create_test_stack()

    if not template.find_resources("AWS::ElasticLoadBalancingV2::LoadBalancer"):
        return

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

    if not template.find_resources("AWS::ECS::TaskDefinition"):
        return

    template.has_resource_properties("AWS::ECS::TaskDefinition", {
        "ContainerDefinitions": [
            {
                "Privileged": Match.absent(),
            }
        ]
    })


def test_fargate_security():
    """Test that Fargate is used for container security if task definitions are deployed"""
    stack, template, config = _create_test_stack()

    if not template.find_resources("AWS::ECS::TaskDefinition"):
        return

    template.has_resource_properties("AWS::ECS::TaskDefinition", {
        "RequiresCompatibilities": ["FARGATE"],
        "NetworkMode": "awsvpc"
    })


def test_ecs_container_insights():
    """Test that ECS cluster has Container Insights enabled if deployed"""
    stack, template, config = _create_test_stack()

    if not template.find_resources("AWS::ECS::Cluster"):
        return

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

    if not template.find_resources("AWS::ElasticLoadBalancingV2::LoadBalancer"):
        return

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

    opensearch_resources = template.find_resources("AWS::OpenSearchService::Domain")
    if not opensearch_resources:
        return

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

    opensearch_resources = template.find_resources("AWS::OpenSearchService::Domain")
    for resource_id, resource in opensearch_resources.items():
        assert resource.get("DeletionPolicy") == "Delete"

    log_group_resources = template.find_resources("AWS::Logs::LogGroup")
    for resource_id, resource in log_group_resources.items():
        assert resource.get("DeletionPolicy") == "Delete"


def test_cloudfront_https_enforcement():
    """Test that the CloudFront distribution enforces HTTPS via redirect on the default behavior if deployed"""
    stack, template, config = _create_test_stack()

    if not template.find_resources("AWS::CloudFront::Distribution"):
        return

    template.has_resource_properties("AWS::CloudFront::Distribution", {
        "DistributionConfig": {
            "DefaultCacheBehavior": {
                "ViewerProtocolPolicy": "redirect-to-https"
            }
        }
    })


# Application Load Balancer Security Configuration Tests
def test_alb_https_listener_uses_strong_tls_policy():
    """Test that the ALB HTTPS listener uses the required strong TLS policy"""
    stack, template, config = _create_test_stack()

    template.has_resource_properties("AWS::ElasticLoadBalancingV2::Listener", {
        "Port": 443,
        "Protocol": "HTTPS",
        "SslPolicy": "ELBSecurityPolicy-TLS13-1-2-Res-2021-06"
    })


def test_alb_listener_enforces_hsts_preload_header():
    """Test that the ALB HTTPS listener injects the required HSTS preload header"""
    stack, template, config = _create_test_stack()

    template.has_resource_properties("AWS::ElasticLoadBalancingV2::Listener", {
        "ListenerAttributes": [
            {
                "Key": "routing.http.response.strict_transport_security.header_value",
                "Value": "max-age=31536000; includeSubDomains; preload"
            },
            {
                "Key": "routing.http.response.x_content_type_options.header_value",
                "Value": "nosniff"
            },
            {
                "Key": "routing.http.response.server.enabled",
                "Value": "false"
            }
        ]
    })


def test_alb_listener_enforces_x_content_type_options_header():
    """Test that the ALB HTTPS listener injects X-Content-Type-Options nosniff"""
    stack, template, config = _create_test_stack()

    template.has_resource_properties("AWS::ElasticLoadBalancingV2::Listener", {
        "ListenerAttributes": [
            {
                "Key": "routing.http.response.x_content_type_options.header_value",
                "Value": "nosniff"
            }
        ]
    })


def test_alb_listener_disables_server_header():
    """Test that the ALB Server response header is disabled"""
    stack, template, config = _create_test_stack()

    template.has_resource_properties("AWS::ElasticLoadBalancingV2::Listener", {
        "ListenerAttributes": [
            {
                "Key": "routing.http.response.server.enabled",
                "Value": "false"
            }
        ]
    })


def test_alb_http_redirects_to_https():
    """Test that HTTP traffic is redirected to HTTPS"""
    stack, template, config = _create_test_stack()

    template.has_resource_properties("AWS::ElasticLoadBalancingV2::Listener", {
        "Port": 80,
        "Protocol": "HTTP",
        "DefaultActions": [
            {
                "Type": "redirect",
                "RedirectConfig": {
                    "Protocol": "HTTPS",
                    "Port": "443"
                }
            }
        ]
    })


def test_alb_https_listener_has_safe_default_404_response():
    """Test that the HTTPS listener default action returns 404 instead of exposing backend details"""
    stack, template, config = _create_test_stack()

    template.has_resource_properties("AWS::ElasticLoadBalancingV2::Listener", {
        "Port": 443,
        "DefaultActions": [
            {
                "Type": "fixed-response",
                "FixedResponseConfig": {
                    "StatusCode": "404",
                    "ContentType": "text/plain",
                    "MessageBody": "Not Found"
                }
            }
        ]
    })


def test_no_public_ingress_to_services():
    """Test that only the ALB accepts inbound traffic from the public internet (ports 80 and 443)"""
    stack, template, config = _create_test_stack()

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

        assert from_port in [80, 443] and to_port in [80, 443]


if __name__ == "__main__":
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
