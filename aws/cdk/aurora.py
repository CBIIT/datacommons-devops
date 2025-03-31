from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_rds as rds,
)

class AuroraMySQLStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, vpc_id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Import existing VPC
        vpc = ec2.Vpc.from_lookup(self, "ImportedVPC", vpc_id=vpc_id)

        # Create a subnet group for Aurora
        subnet_group = rds.SubnetGroup(
            self, "AuroraSubnetGroup",
            vpc=vpc,
            description="Subnet group for Aurora MySQL cluster",
            removal_policy=core.RemovalPolicy.DESTROY  # Modify as per requirements
        )

        # Aurora MySQL Cluster
        cluster = rds.DatabaseCluster(
            self, "AuroraCluster",
            engine=rds.DatabaseClusterEngine.aurora_mysql(version=rds.AuroraMysqlEngineVersion.VER_8_0),
            instances=2,  # Multi-AZ for high availability
            vpc=vpc,
            subnet_group=subnet_group,
            default_database_name="mydatabase",
            storage_encrypted=True,  # Encryption enabled as per AWS best practices
            deletion_protection=True,  # Protect against accidental deletion
            backup=rds.BackupProps(retention=core.Duration.days(7)),  # Backup retention for disaster recovery
        )

app = core.App()
AuroraMySQLStack(app, "AuroraMySQLStack", vpc_id="vpc-12345678")  # Replace with actual VPC ID
app.synth()
