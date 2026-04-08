from configparser import ConfigParser, ExtendedInterpolation
from constructs import Construct
from aws_cdk import Stack, Duration, RemovalPolicy
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_kms as kms
# from aws_cdk import aws_iam as iam
from aws_cdk import aws_rds as rds
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_certificatemanager as cfm
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_secretsmanager as secretsmanager
from aws_cdk import SecretValue

# from services import memgraph

# Read config
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read("config.ini")

class Stack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.namingPrefix = "{}-{}".format(config['main']['resource_prefix'], config['main']['tier'])

        # Import VPC
        self.VPC = ec2.Vpc.from_lookup(
            self,
            "VPC",
            vpc_id=config["main"]["vpc_id"]
        )

        # Phoenix Service
        service = "phoenix"

        ### Secrets
        self.secret = secretsmanager.Secret(
            self,
            "Secret",
            secret_name=f"{config['main']['program']}/{config['main']['project']}/{config['main']['tier']}",
            secret_object_value={
                "phoenix_secret": SecretValue.unsafe_plain_text(config[service]['phoenix_secret']),
                "phoenix_admin_password": SecretValue.unsafe_plain_text(config[service]['phoenix_admin_password']),
                "username": SecretValue.unsafe_plain_text(config['db']['db_user']),
                "password": SecretValue.unsafe_plain_text(config['db']['db_pass']),
                "dbname": SecretValue.unsafe_plain_text(config['db']['db_name']),
            }
        )
        
        # RDS
        self.postgres = rds.DatabaseInstance(self, "Postgres",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_16
            ),
            vpc=self.VPC,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.MICRO,
            ),
            # credentials=rds.Credentials.from_generated_secret("postgres"),
            credentials=rds.Credentials.from_secret(self.secret),
            database_name=config["db"]["db_name"],
            allocated_storage=20,
            max_allocated_storage=100,
            multi_az=False,
            publicly_accessible=False,
            storage_encrypted=True,
            backup_retention=Duration.days(7),
            deletion_protection=False,
            removal_policy=RemovalPolicy.DESTROY,
            delete_automated_backups=True,
        )

        # ECS Cluster
        self.kmsKey = kms.Key(self, "ECSExecKey")

        self.ECSCluster = ecs.Cluster(
            self,
            "ecs",
            vpc=self.VPC,
            execute_command_configuration=ecs.ExecuteCommandConfiguration(
                kms_key=self.kmsKey
            ),
        )
        
        # Set container configs
        if config.has_option(service, 'entry_point'):
            entry_point = ["/bin/sh", "-c", config[service]['entry_point']]
        else:
            entry_point = None

        secrets={
            "PHOENIX_SECRET":ecs.Secret.from_secrets_manager(self.secret, 'phoenix_secret'),
            "PHOENIX_DEFAULT_ADMIN_INITIAL_PASSWORD":ecs.Secret.from_secrets_manager(self.secret, 'phoenix_admin_password'),
            "PHOENIX_SQL_DATABASE_USER":ecs.Secret.from_secrets_manager(self.secret, 'username'),
            "PHOENIX_SQL_DATABASE_PASSWORD":ecs.Secret.from_secrets_manager(self.secret, 'password'),
            "PHOENIX_SQL_DATABASE_NAME":ecs.Secret.from_secrets_manager(self.secret, 'dbname')
        }

        environment={
            "PHOENIX_SQL_DATABASE_HOST": self.postgres.db_instance_endpoint_address,
            "PHOENIX_TELEMETRY_ENABLED": "false",
            "PHOENIX_ENABLE_AUTH": "true",
            "PHOENIX_SQL_DATABASE_SCHEMA": "postgresql",
            "PHOENIX_SQL_DATABASE_PORT": "5432"
        }

        taskDefinition = ecs.FargateTaskDefinition(self,
            "{}-{}-taskDef".format(self.namingPrefix, service),
            cpu=config.getint(service, 'cpu'),
            memory_limit_mib=config.getint(service, 'memory')
        )

        phoenixContainer = taskDefinition.add_container(
            service,
            image=ecs.ContainerImage.from_registry(config[service]['image']),
            cpu=config.getint(service, 'cpu'),
            memory_limit_mib=config.getint(service, 'memory'),
            port_mappings=[ecs.PortMapping(container_port=config.getint(service, 'port'), name=service)],
            # user="root",
            entry_point=entry_point,
            secrets=secrets,
            environment=environment,
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="{}-{}".format(self.namingPrefix, service)
            )
        )

        ecsService = ecs.FargateService(self,
            "{}-{}-service".format(self.namingPrefix, service),
            cluster=self.ECSCluster,
            task_definition=taskDefinition,
            enable_execute_command=True,
            min_healthy_percent=0,
            max_healthy_percent=100,
            circuit_breaker=ecs.DeploymentCircuitBreaker(
                enable=True,
                rollback=True
            )
        )

        ### ALB
        if config.getboolean('alb', 'internet_facing'):
            subnets=ec2.SubnetSelection(
                subnets=self.VPC.select_subnets(one_per_az=True,subnet_type=ec2.SubnetType.PUBLIC).subnets
            )
        else:
            subnets=ec2.SubnetSelection(
                subnets=self.VPC.select_subnets(one_per_az=True,subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnets
            )

        # ALB
        self.ALB = elbv2.ApplicationLoadBalancer(self,
            "alb",
            vpc=self.VPC,
            internet_facing=config.getboolean('alb', 'internet_facing'),
            vpc_subnets=subnets
        )

        self.ALB.log_access_logs(
            prefix=f"{config['main']['program']}/{config['main']['tier']}/{config['main']['project']}/alb-access-logs",
            bucket=s3.Bucket.from_bucket_arn(self,
                f"{self.namingPrefix}-ALB-CentralLogBucket",
                bucket_arn=config['alb']['log_bucket_arn']
            )
        )

        self.ALB.add_redirect(
            source_protocol=elbv2.ApplicationProtocol.HTTP,
            source_port=80,
            target_protocol=elbv2.ApplicationProtocol.HTTPS,
            target_port=443
        )

        alb_cert = cfm.Certificate.from_certificate_arn(self, "alb-cert",
            certificate_arn=config['alb']['certificate_arn']
        )
        
        self.listener = self.ALB.add_listener("PublicListener",
            certificates=[alb_cert],
            port=443
        )

        ecsService.connections.allow_to_default_port(self.postgres)

        ecsTarget = self.listener.add_targets("ECS-{}-Target".format(service),
            port=int(config[service]['port']),
            protocol=elbv2.ApplicationProtocol.HTTP,
            health_check = elbv2.HealthCheck(
                path=config[service]['health_check_path'],
                timeout=Duration.seconds(config.getint(service, 'health_check_timeout')),
                interval=Duration.seconds(config.getint(service, 'health_check_interval')),),
            targets=[ecsService],)

        elbv2.ApplicationListenerRule(self, id="alb-{}-rule".format(service),
            conditions=[
                elbv2.ListenerCondition.path_patterns(config[service]['path'].split(','))
            ],
            priority=int(config[service]['priority_rule_number']),
            listener=self.listener,
            target_groups=[ecsTarget]
        )

        self.listener.add_action("ECS-Content-Not-Found",
            action=elbv2.ListenerAction.fixed_response(200,
                message_body="The requested resource is not available")
        )