from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins
)

class CloudFrontS3Stack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, *, vpc_id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Import existing VPC
        vpc = ec2.Vpc.from_lookup(self, "ImportedVPC", vpc_id=vpc_id)

        # Create an S3 bucket
        bucket = s3.Bucket(self, "CloudFrontS3Bucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=core.RemovalPolicy.RETAIN
        )

        # Create a CloudFront distribution
        distribution = cloudfront.Distribution(self, "CloudFrontDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            ),
            price_class=cloudfront.PriceClass.PRICE_CLASS_100,
            http_version=cloudfront.HttpVersion.HTTP2_AND_3
        )

        core.CfnOutput(self, "CloudFrontDistributionDomainName", value=distribution.domain_name)

app = core.App()
CloudFrontS3Stack(app, "CloudFrontS3Stack", vpc_id="vpc-12345678")
app.synth()