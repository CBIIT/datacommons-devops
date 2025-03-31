from aws_cdk import core
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_elasticloadbalancingv2 as elb

class NlbStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Network Load Balancer
        nlb = elb.NetworkLoadBalancer(self, 
            "MyNLB",
            vpc=vpc,
            internet_facing=True  # Expose the NLB to the internet (can be changed based on needs)
        )

        # Add a listener to the NLB
        listener = nlb.add_listener(
            "Listener",
            port=80,  # HTTP traffic on port 80 (can change to 443 for HTTPS)
            open=True  # Allow open access (you may wish to add specific access control later)
        )

        # Here, you would add targets like EC2 instances or auto scaling groups
        # Example:
        # listener.add_targets("MyTargets", port=80, targets=[ec2.Instance(self, "MyInstance")])

        # The load balancer will be created in the VPC provided
        # You can configure it further by adding additional listeners, target groups, etc.
        core.CfnOutput(self, "NLBUrl", value=nlb.load_balancer_dns_name)
