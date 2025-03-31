from aws_cdk import (
    core as cdk,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_certificatemanager as acm
)

class AlbStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Import an existing VPC
        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=False)

        # Import an existing certificate from AWS Certificate Manager (ACM)
        certificate_arn = "arn:aws:acm:region:account-id:certificate/certificate-id"  # Replace with actual ARN
        certificate = acm.Certificate.from_certificate_arn(self, "Certificate", certificate_arn)

        # Create an Application Load Balancer
        alb = elbv2.ApplicationLoadBalancer(
            self, "ALB",
            vpc=vpc,
            internet_facing=True
        )
        
        # Add a listener with HTTPS
        listener = alb.add_listener("Listener",
            port=443,
            certificates=[certificate],
            open=True  # Security groups should be added separately
        )

        # Default action - Fixed response when accessing invalid URLs
        listener.add_action("DefaultAction",
            action=elbv2.ListenerAction.fixed_response(
                status_code=elbv2.HttpStatusCode.NOT_FOUND,
                content_type=elbv2.ContentType.TEXT_PLAIN,
                message_body="The page you requested could not be found."
            )
        )
        
        # Output ALB DNS name
        cdk.CfnOutput(self, "ALBDNSName", value=alb.load_balancer_dns_name)

app = cdk.App()
AlbStack(app, "AlbStack")
app.synth()
# This code creates an Application Load Balancer (ALB) in an existing VPC. The ALB is configured with an HTTPS listener using an existing SSL certificate from AWS Certificate Manager (ACM).