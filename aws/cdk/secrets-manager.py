from aws_cdk import (
    core,
    aws_secretsmanager as secretsmanager,
    aws_ec2 as ec2
)

class SecretsManagerStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, *, vpc_id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Import existing VPC
        vpc = ec2.Vpc.from_lookup(self, "ImportedVPC", vpc_id=vpc_id)

        # Create a Secrets Manager secret
        secret = secretsmanager.Secret(self, "MySecret",
            description="A secret stored securely in AWS Secrets Manager.",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template="{\"username\": \"admin\"}",
                generate_string_key="password",
                exclude_punctuation=True  # Improves compatibility with various services
            )
        )

        core.CfnOutput(self, "SecretArn", value=secret.secret_arn, description="ARN of the created secret")

app = core.App()
SecretsManagerStack(app, "SecretsManagerStack", vpc_id="vpc-12345678")  # Replace with your actual VPC ID
app.synth()