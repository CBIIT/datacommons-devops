from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_opensearchservice as opensearch
)

class OpenSearchStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, *, vpc_id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Import existing VPC
        vpc = ec2.Vpc.from_lookup(self, "ImportedVPC", vpc_id=vpc_id)

        # Select private subnets for OpenSearch domain
        subnet_selection = ec2.SubnetSelection(
            subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT
        )

        # Create OpenSearch Domain
        domain = opensearch.CfnDomain(
            self, "OpenSearchCluster",
            elasticsearch_version="7.10",
            vpc_options=opensearch.CfnDomain.VPCOptionsProperty(
                subnet_ids=[subnet.subnet_id for subnet in vpc.private_subnets]
            ),
            node_to_node_encryption_options={"enabled": True},
            encryption_at_rest_options={"enabled": True},
            cluster_config={
                "instance_type": "t3.medium.search",
                "instance_count": 2,
                "zone_awareness_enabled": True,
                "zone_awareness_config": {"availability_zone_count": 2}
            },
            ebs_options={
                "ebs_enabled": True,
                "volume_size": 10
            }
        )

        core.CfnOutput(self, "OpenSearchDomainEndpoint", value=domain.attr_endpoint)

app = core.App()
OpenSearchStack(app, "OpenSearchStack", vpc_id="vpc-12345678")
app.synth()
    
    # This code creates an OpenSearch domain in an existing VPC. The domain is configured with two t3.medium.search instances, 10 GB of EBS storage, and zone awareness across two availability zones. 
    # To deploy this stack, save the code in a file named  opensearch.py  and run the following commands: 
    # $ python3 -m venv .venv