from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_secretsmanager as secretsmanager,
    aws_lb as elb,
    aws_iam as iam,
    aws_ssm as ssm,
)

class EcsFargateServiceStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Import existing VPC
        vpc = ec2.Vpc.from_lookup(self, "ImportedVPC", vpc_id="vpc-xxxxxxxxxxxxxxx")  # Replace with your VPC ID

        # Create ECS Cluster
        cluster = ecs.Cluster(self, "EcsCluster", vpc=vpc)

        # Define task definition
        task_definition = ecs.FargateTaskDefinition(self, "FargateTaskDefinition", memory_limit_mib=2048, cpu=1024)

        # Define a container with environment variables and secrets
        container = task_definition.add_container(
            "MyContainer",
            image=ecs.ContainerImage.from_registry("my-docker-image:latest"),  # Use your image
            environment={
                "MY_ENV_VAR": "value",  # Example of environment variable
            },
            secrets={
                "MY_SECRET": ecs.Secret.from_secrets_manager(secretsmanager.Secret.from_secret_name_v2(self, "MySecret", "my-secret-name")),  # Reference to a secret from Secrets Manager
            },
        )

        # Create Application Load Balancer
        alb = elb.ApplicationLoadBalancer(self, "MyALB", vpc=vpc, internet_facing=True)

        # Define a listener for the ALB
        listener = alb.add_listener("Listener", port=80)

        # Create a target group
        target_group = listener.add_targets("EcsTargets", port=80, targets=[ecs_patterns.NetworkLoadBalancedFargateService(self, "FargateService", 
            cluster=cluster,
            task_definition=task_definition,
            public_load_balancer=True
        ).load_balancer])

        # ECS Fargate service connected to the ALB
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "FargateService",
            cluster=cluster,
            task_definition=task_definition,
            public_load_balancer=True,
        )

        # Define CloudWatch Logs, ALB logging, and other monitoring resources to support Well-Architected best practices (Optional but recommended)
        fargate_service.task_definition.add_container("Container", image=ecs.ContainerImage.from_registry("nginx"))
        
        # Optional: Enable CloudWatch logging and monitoring
        container.add_log_driver(
            ecs.LogDriver.aws_logs(stream_prefix="my-logs")
        )


app = core.App()
EcsFargateServiceStack(app, "EcsFargateServiceStack")
app.synth()
