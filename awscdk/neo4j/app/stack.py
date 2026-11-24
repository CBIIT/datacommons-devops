from configparser import ConfigParser
from constructs import Construct

from aws_cdk import Stack
from aws_cdk import RemovalPolicy
from aws_cdk import SecretValue
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_kms as kms
from aws_cdk import aws_secretsmanager as secretsmanager
from aws_cdk import aws_efs as efs
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_s3 as s3

from services import neo4j

class Stack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ### Read config
        config = ConfigParser()
        config.read('config.ini')
        
        self.namingPrefix = "{}-{}".format(config['main']['resource_prefix'], config['main']['tier'])

        ### Import VPC
        self.VPC = ec2.Vpc.from_lookup(self, "VPC",
            vpc_id = config['main']['vpc_id']
        )

        ### Secrets
        self.secret = secretsmanager.Secret(self, "Secret",
            secret_name="{}/{}".format(config['main']['resource_prefix'], config['main']['tier']),
            secret_object_value={
                "neo4j_user": SecretValue.unsafe_plain_text(config['db']['neo4j_user']),
                "neo4j_password": SecretValue.unsafe_plain_text(config['db']['neo4j_password']),
            }
        )

        ### EFS - Neo4j
        EFSSecurityGroup = ec2.SecurityGroup(self, "EFSSecurityGroup", vpc=self.VPC, allow_all_outbound=True,)
        EFSSecurityGroup.add_ingress_rule(peer=ec2.Peer.ipv4(self.VPC.vpc_cidr_block),
            connection=ec2.Port.tcp(2049),
        )
        self.fileSystem = efs.FileSystem(self, "EfsFileSystem",
            vpc=self.VPC,
            encrypted=True,
            enable_automatic_backups=True,
            security_group=EFSSecurityGroup,
            removal_policy=RemovalPolicy.DESTROY
        )
        self.EFSAccessPoint = self.fileSystem.add_access_point("EFSAccessPoint",
            path="/{}".format(config['main']['tier']),
            create_acl=efs.Acl(
                owner_uid="7474",
                owner_gid="7474",
                permissions="755"
            ),
            posix_user=efs.PosixUser(
                uid="7474",
                gid="7474"
            )
        )
        self.EFSPluginAccessPoint = self.fileSystem.add_access_point("EFSPluginAccessPoint",
            path="/{}/plugins".format(config['main']['tier']),
            create_acl=efs.Acl(
                owner_uid="7474",
                owner_gid="7474",
                permissions="755"
            ),
            posix_user=efs.PosixUser(
                uid="7474",
                gid="7474"
            )
        )

        ### ECS Cluster
        self.kmsKey = kms.Key(self, "ECSExecKey")

        self.ECSCluster = ecs.Cluster(self,
            "ecs",
            cluster_name = f"{config['main']['resource_prefix']}-{config['main']['tier']}-ecs",
            vpc=self.VPC,
            execute_command_configuration=ecs.ExecuteCommandConfiguration(
                kms_key=self.kmsKey
            ),
        )

        ### Fargate

        # Neo4j Service
        neo4j.neo4jService.createService(self, config)