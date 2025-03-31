from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_efs as efs,
)

class EfsStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, vpc: ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create EFS filesystem in the VPC
        efs_filesystem = efs.FileSystem(
            self, 
            "EFSFileSystem", 
            vpc=vpc,
            removal_policy=core.RemovalPolicy.DESTROY,  # Ensures EFS is deleted when stack is destroyed
            lifecycle_policy=efs.LifecyclePolicy.AFTER_7_DAYS,  # Moves files to infrequent access after 7 days
            performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,  # Best for most workloads
            throughput_mode=efs.ThroughputMode.BURSTING,  # Scales throughput automatically
        )
        
        # Add mount targets for the VPC subnets
        efs_filesystem.add_mount_target(
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)  # Mount in public subnet
        )
        efs_filesystem.add_mount_target(
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE)  # Mount in private subnet
        )

        # Optional: Outputs for EFS details
        core.CfnOutput(self, "EFSId", value=efs_filesystem.file_system_id)
        core.CfnOutput(self, "EFSMountTarget", value=efs_filesystem.mount_targets[0].dns_name)


# Assuming you are using a VPC imported
app = core.App()

# Import existing VPC by ID or name
vpc = ec2.Vpc.from_lookup(app, "ImportedVPC", vpc_id="vpc-xxxxxxxx")

efs_stack = EfsStack(app, "EfsStack", vpc=vpc)

app.synth()
