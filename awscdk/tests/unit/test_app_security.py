import re

import aws_cdk as cdk
from aws_cdk.assertions import Template, Match

from configparser import ConfigParser

from app import build_stack


def _is_secure_tls_policy(ssl_policy):
    """AWS ELB security policy names encode their minimum TLS version (e.g. '...-1-2-...').
    Accept any policy whose minimum is TLS 1.2 or 1.3; reject ones permitting TLS 1.0/1.1."""
    return bool(re.search(r"-1-[23]-", ssl_policy)) and not re.search(r"-1-[01]-", ssl_policy)


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

    # Check every role, not just one, since MyAspect is expected to rename all of them
    role_resources = template.find_resources("AWS::IAM::Role")
    assert role_resources, "Expected at least one IAM::Role in the stack"
    for resource_id, resource in role_resources.items():
        role_name = resource.get("Properties", {}).get("RoleName")
        assert isinstance(role_name, str) and role_name.startswith(f"{expected_prefix}-"), (
            f"Role {resource_id} RoleName '{role_name}' does not start with expected prefix '{expected_prefix}-'"
        )


def test_permission_boundaries():
    """Test that permission boundaries are applied to IAM roles for security compliance"""
    stack, template, config = _create_test_stack()

    if not config.has_option('iam', 'permission_boundary'):
        return

    # Every role must carry the boundary, not just one
    expected_boundary = config['iam']['permission_boundary']
    role_resources = template.find_resources("AWS::IAM::Role")
    assert role_resources, "Expected at least one IAM::Role in the stack"
    for resource_id, resource in role_resources.items():
        boundary = resource.get("Properties", {}).get("PermissionsBoundary")
        assert boundary == expected_boundary, (
            f"Role {resource_id} PermissionsBoundary '{boundary}' does not match expected '{expected_boundary}'"
        )


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


def test_iam_policies_no_wildcard_actions():
    """Test that IAM policy documents do not grant blanket wildcard actions"""
    stack, template, config = _create_test_stack()

    disallowed_actions = {"*", "iam:*", "s3:*"}

    for resource_id, resource in template.find_resources("AWS::IAM::Policy").items():
        statements = resource.get("Properties", {}).get("PolicyDocument", {}).get("Statement", [])
        for statement in statements:
            if statement.get("Effect") != "Allow":
                continue
            actions = statement.get("Action", [])
            actions = actions if isinstance(actions, list) else [actions]
            offending = disallowed_actions.intersection(actions)
            assert not offending, f"{resource_id} grants disallowed wildcard action(s) {offending}"


def test_container_secrets_security():
    """Test that containers retrieve secrets securely from Secrets Manager if deployed"""
    stack, template, config = _create_test_stack()

    # Only test if task definitions with secrets are deployed
    task_def_resources = template.find_resources("AWS::ECS::TaskDefinition")
    if not task_def_resources:
        return

    # Inspect every container (including sidecars) rather than matching the
    # ContainerDefinitions array exactly, since that array's length varies
    # depending on how many sidecar containers a task definition has.
    found_secure_secret = False
    for resource_id, resource in task_def_resources.items():
        containers = resource.get("Properties", {}).get("ContainerDefinitions", [])
        for container in containers:
            for secret in container.get("Secrets", []):
                assert "Fn::Join" in secret.get("ValueFrom", {}), (
                    f"{resource_id} container '{container.get('Name')}' secret "
                    f"'{secret.get('Name')}' must reference Secrets Manager via Fn::Join"
                )
                found_secure_secret = True

    assert found_secure_secret, "Expected at least one container to retrieve secrets from Secrets Manager"


def test_kms_key_policy_least_privilege():
    """Test that customer-managed KMS keys restrict access to least privilege if deployed"""
    stack, template, config = _create_test_stack()

    kms_resources = template.find_resources("AWS::KMS::Key")
    if not kms_resources:
        return

    # Control-plane/admin actions a non-root principal should never hold; usage actions
    # (Decrypt/Encrypt/GenerateDataKey/CreateGrant and their many wildcard-suffixed AWS-service
    # variants, e.g. ECS Exec's "kms:Decrypt*") are intentionally not enumerated here since AWS
    # services legitimately emit new variants over time.
    dangerous_kms_actions = {
        "kms:PutKeyPolicy", "kms:GetKeyPolicy", "kms:ScheduleKeyDeletion", "kms:DisableKey",
        "kms:EnableKeyRotation", "kms:DisableKeyRotation", "kms:RevokeGrant", "kms:TagResource",
        "kms:UntagResource", "kms:CreateKey", "kms:DeleteAlias", "kms:UpdateAlias",
        "kms:UpdateKeyDescription", "kms:ImportKeyMaterial", "kms:DeleteImportedKeyMaterial",
        "kms:ReplicateKey", "kms:UpdatePrimaryRegion",
    }

    def _is_dangerous_action(action):
        if action in ("*", "kms:*"):
            return True
        if action.endswith("*"):
            prefix = action[:-1]
            return any(dangerous.startswith(prefix) for dangerous in dangerous_kms_actions)
        return action in dangerous_kms_actions

    def _actions(statement):
        actions = statement.get("Action", [])
        return actions if isinstance(actions, list) else [actions]

    def _is_root_principal(statement):
        principal = statement.get("Principal", {})
        aws_principal = principal.get("AWS", {}) if isinstance(principal, dict) else {}
        # CDK renders the root principal via an Fn::Join/Fn::Sub containing ":root"
        return "root" in str(aws_principal)

    for resource_id, resource in kms_resources.items():
        statements = resource.get("Properties", {}).get("KeyPolicy", {}).get("Statement", [])
        assert statements, f"KMS key {resource_id} should have a key policy with statements"

        has_root_full_access = False
        for statement in statements:
            actions = _actions(statement)
            if _is_root_principal(statement) and "kms:*" in actions:
                has_root_full_access = True
                continue

            # Non-root principals (e.g. cross-account roles) must never get a wildcard action
            assert "*" not in actions and "kms:*" not in actions, (
                f"KMS key {resource_id} grants a non-root principal a wildcard action: {actions}"
            )
            dangerous = [action for action in actions if _is_dangerous_action(action)]
            assert not dangerous, (
                f"KMS key {resource_id} grants a non-root principal administrative/control-plane "
                f"actions: {dangerous}"
            )

        assert has_root_full_access, f"KMS key {resource_id} should grant the account root full access"


def test_secrets_manager_resource_policy_least_privilege():
    """Test that Secrets Manager resource policies restrict access to GetSecretValue only if deployed"""
    stack, template, config = _create_test_stack()

    policy_resources = template.find_resources("AWS::SecretsManager::ResourcePolicy")
    if not policy_resources:
        return

    for resource_id, resource in policy_resources.items():
        statements = resource.get("Properties", {}).get("ResourcePolicy", {}).get("Statement", [])
        assert statements, f"Secrets Manager resource policy {resource_id} should have statements"

        for statement in statements:
            actions = statement.get("Action", [])
            actions = actions if isinstance(actions, list) else [actions]
            assert actions and set(actions) == {"secretsmanager:GetSecretValue"}, (
                f"{resource_id} statement should only allow secretsmanager:GetSecretValue, found {actions}"
            )

            principal = statement.get("Principal", {})
            assert principal != "*", f"{resource_id} must not grant access to a wildcard principal"
            if isinstance(principal, dict):
                assert principal.get("AWS") != "*", f"{resource_id} must not grant access to a wildcard AWS principal"


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
    """Test that ALB uses a security policy enforcing a secure minimum TLS version if deployed"""
    stack, template, config = _create_test_stack()

    # Only test if an ALB is deployed
    if not template.find_resources("AWS::ElasticLoadBalancingV2::LoadBalancer"):
        return

    https_listeners = {
        resource_id: resource
        for resource_id, resource in template.find_resources("AWS::ElasticLoadBalancingV2::Listener").items()
        if resource.get("Properties", {}).get("Port") == 443
    }
    assert https_listeners, "Expected at least one HTTPS listener"

    # Accept any security policy that enforces a minimum of TLS 1.2 (e.g. the
    # default, Res, Ext1/Ext2, or FIPS variants), not just one exact policy name
    for resource_id, resource in https_listeners.items():
        ssl_policy = resource.get("Properties", {}).get("SslPolicy")
        assert ssl_policy and _is_secure_tls_policy(ssl_policy), (
            f"{resource_id} SslPolicy '{ssl_policy}' does not enforce a minimum of TLS 1.2"
        )


def _https_listener_attributes(template):
    """Return {listener_resource_id: {attribute_key: attribute_value}} for every port-443 listener."""
    https_listeners = {
        resource_id: resource
        for resource_id, resource in template.find_resources("AWS::ElasticLoadBalancingV2::Listener").items()
        if resource.get("Properties", {}).get("Port") == 443
    }
    assert https_listeners, "Expected at least one HTTPS listener"
    return {
        resource_id: {
            attribute.get("Key"): attribute.get("Value")
            for attribute in resource.get("Properties", {}).get("ListenerAttributes", [])
        }
        for resource_id, resource in https_listeners.items()
    }


def test_alb_listener_enforces_hsts_preload_header():
    """Test that the ALB HTTPS listener injects the required HSTS preload header if deployed"""
    stack, template, config = _create_test_stack()

    if not template.find_resources("AWS::ElasticLoadBalancingV2::LoadBalancer"):
        return

    for resource_id, attributes in _https_listener_attributes(template).items():
        assert attributes.get("routing.http.response.strict_transport_security.header_value") == (
            "max-age=31536000; includeSubDomains; preload"
        ), f"{resource_id} does not enforce the required HSTS preload header"


def test_alb_listener_enforces_x_content_type_options_header():
    """Test that the ALB HTTPS listener injects X-Content-Type-Options: nosniff if deployed"""
    stack, template, config = _create_test_stack()

    if not template.find_resources("AWS::ElasticLoadBalancingV2::LoadBalancer"):
        return

    for resource_id, attributes in _https_listener_attributes(template).items():
        assert attributes.get("routing.http.response.x_content_type_options.header_value") == "nosniff", (
            f"{resource_id} does not set X-Content-Type-Options: nosniff"
        )


def test_alb_listener_disables_server_header():
    """Test that the ALB HTTPS listener disables the Server response header if deployed"""
    stack, template, config = _create_test_stack()

    if not template.find_resources("AWS::ElasticLoadBalancingV2::LoadBalancer"):
        return

    for resource_id, attributes in _https_listener_attributes(template).items():
        assert attributes.get("routing.http.response.server.enabled") == "false", (
            f"{resource_id} does not disable the Server response header"
        )


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

    # A KeyGroup/PublicKey existing on their own enforce nothing — the distribution's
    # default behavior must actually reference the key group to require signed URLs
    template.has_resource_properties("AWS::CloudFront::Distribution", {
        "DistributionConfig": {
            "DefaultCacheBehavior": {
                "TrustedKeyGroups": Match.any_value()
            }
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
    task_def_resources = template.find_resources("AWS::ECS::TaskDefinition")
    if not task_def_resources:
        return

    # Check every container (including sidecars) individually rather than matching
    # the ContainerDefinitions array exactly, since its length varies with sidecars,
    # and so that every sidecar is held to the same "not privileged" requirement.
    for resource_id, resource in task_def_resources.items():
        containers = resource.get("Properties", {}).get("ContainerDefinitions", [])
        for container in containers:
            assert "Privileged" not in container, (
                f"{resource_id} container '{container.get('Name')}' should not be privileged"
            )
            # "ReadonlyRootFilesystem": Match.any_value(),
            # "User": Match.any_value()


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
    # Run all security tests
    security_test_functions = [
        test_opensearch_encryption,
        test_opensearch_access_policies,
        test_opensearch_vpc_security,
        test_opensearch_single_az_security,
        test_iam_role_naming_aspect,
        test_permission_boundaries,
        test_iam_role_trust_policies,
        test_iam_policies_no_wildcard_actions,
        test_container_secrets_security,
        test_kms_key_policy_least_privilege,
        test_secrets_manager_resource_policy_least_privilege,
        test_alb_https_enforcement,
        test_alb_ssl_certificate,
        test_alb_security_policy,
        test_alb_listener_enforces_hsts_preload_header,
        test_alb_listener_enforces_x_content_type_options_header,
        test_alb_listener_disables_server_header,
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
