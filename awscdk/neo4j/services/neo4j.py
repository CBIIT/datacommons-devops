import aws_cdk

from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_secretsmanager as secretsmanager
from datetime import date
from aws_cdk import Duration
from aws_cdk import aws_iam as iam
from aws_cdk import CfnOutput

class neo4jService:
  def createService(self, config):

    ### Neo4j Service ###############################################################################################################
    service = "neo4j"

    # Set container configs
    if config.has_option(service, 'entry_point'):
        entry_point = ["/bin/sh", "-c", config[service]['entry_point']]
    else:
        entry_point = None

    # Extract subnet IDs
    subnet_nlb1 = config.get('Subnets', 'subnet_nlb1')
    subnet_nlb2 = config.get('Subnets', 'subnet_nlb2')
    subnets_nlb = ec2.SubnetSelection(
        subnets=[
            ec2.Subnet.from_subnet_id(self, "Subnet_nlb1", subnet_nlb1),
            ec2.Subnet.from_subnet_id(self, "Subnet_nlb2", subnet_nlb2)
        ]
    )

    # read CIDRs and port from config.ini
    restricted_cidrs = config.get(service, 'allowed_cidrs').split(',')

    # create NLB
    self.NLB = elbv2.NetworkLoadBalancer(self,
        "nlb",
        load_balancer_name = f"{config['main']['resource_prefix']}-{config['main']['tier']}-nlb",
        vpc=self.VPC,
        internet_facing=config.getboolean('nlb', 'internet_facing'),
        vpc_subnets=subnets_nlb,
    )

    environment={
        "NEO4J_apoc_export_file_enabled":config['db']['apoc_export_file_enabled'],
        "NEO4J_apoc_import_file_enabled":config['db']['apoc_import_file_enabled'],
        "NEO4J_apoc_import_file_use__neo4j__config":config['db']['apoc_file_use_config'],
        "NEO4J_apoc_trigger_enabled":config['db']['apoc_trigger_enabled'],
        "NEO4J_AUTH":"{}/{}".format(config['db']['neo4j_user'], config['db']['neo4j_password']),

        "NEO4J_dbms_default__advertised__address":"{}".format(self.NLB.load_balancer_dns_name),
        "NEO4J_dbms_connector_http_enabled":"true",
        "NEO4J_dbms_connector_http_listen__address":"0.0.0.0:7474",
        "NEO4J_dbms_connector_http_advertised__address":"{}:7474".format(self.NLB.load_balancer_dns_name),

        "NEO4J_dbms_connector_bolt_enabled":"true",
        "NEO4J_dbms_connector_bolt_listen__address":"0.0.0.0:7687",
        "NEO4J_dbms_connector_bolt_advertised__address":"{}:7687".format(self.NLB.load_balancer_dns_name),

        "NEO4J_ACCEPT_LICENSE_AGREEMENT":"yes",
        "NEO4J_dbms_security_procedures_unrestricted":"apoc.*",
        "NEO4J_dbms_security_procedures_allowlist":"apoc.*",
        "NEO4J_PLUGINS":'["apoc"]'
    }

    dbVolume = ecs.Volume(
        name="neo4j-data",
        efs_volume_configuration=ecs.EfsVolumeConfiguration(
            file_system_id=self.fileSystem.file_system_id,
            authorization_config=ecs.AuthorizationConfig(
                access_point_id=self.EFSAccessPoint.access_point_id,
                iam="ENABLED"
            ),
            transit_encryption="ENABLED"
        )
    )

    pluginVolume = ecs.Volume(
        name="pluginVolume",
        efs_volume_configuration=ecs.EfsVolumeConfiguration(
            file_system_id=self.fileSystem.file_system_id,
            transit_encryption="ENABLED",
            authorization_config=ecs.AuthorizationConfig(
                access_point_id=self.EFSPluginAccessPoint.access_point_id,
                iam="ENABLED"
            )
        )
    )
    
    taskDefinition = ecs.FargateTaskDefinition(self,
        "{}-{}-taskDef".format(self.namingPrefix, service),
        cpu=config.getint(service, 'cpu'),
        memory_limit_mib=config.getint(service, 'memory'),
        volumes=[dbVolume, pluginVolume]
    )

    dbContainer = taskDefinition.add_container(
        service,
        image=ecs.ContainerImage.from_registry("{}:{}".format(config[service]['repo'], config[service]['image'])),
        cpu=config.getint(service, 'cpu'),
        memory_limit_mib=config.getint(service, 'memory'),
        port_mappings=[ecs.PortMapping(container_port=config.getint(service, 'bolt_port'), name="bolt-{}".format(service)), 
            ecs.PortMapping(container_port=config.getint(service, 'http_port'), name="http-{}".format(service))],
        user="root",
        entry_point=entry_point,
        environment=environment,
        logging=ecs.LogDrivers.aws_logs(
            stream_prefix="{}-{}".format(self.namingPrefix, service)
        )
    )

    containerVolumeMountPoint = ecs.MountPoint(
        read_only=False,
        container_path="{}".format(config[service]['data_directory']),
        source_volume=dbVolume.name
    )
    dbContainer.add_mount_points(containerVolumeMountPoint)

    pluginMountPoint = ecs.MountPoint(
        read_only=False,
        container_path="{}".format(config[service]['plugin_directory']),
        source_volume=pluginVolume.name
    )
    dbContainer.add_mount_points(pluginMountPoint)

    self.fileSystem.grant_root_access(taskDefinition.task_role)

    ecsService = ecs.FargateService(self,
        "{}-{}-service".format(self.namingPrefix, service),
        service_name=f"{config['main']['resource_prefix']}-{config['main']['tier']}-neo4j",
        cluster=self.ECSCluster,
        task_definition=taskDefinition,
        enable_execute_command=True,
        min_healthy_percent=0,
        max_healthy_percent=100,
        circuit_breaker=ecs.DeploymentCircuitBreaker(
            enable=True,
            rollback=True
        ),
    )

    #Create Security Group for NLB
    NLBSecurityGroup = ec2.SecurityGroup(self, "NLBSecurityGroup", vpc=self.VPC, allow_all_outbound=True, security_group_name=f"{config['main']['resource_prefix']}-{config['main']['tier']}-nlb-sg",)

    # add ingress rules for each CIDR
    for cidr in restricted_cidrs:
        NLBSecurityGroup.add_ingress_rule(peer=ec2.Peer.ipv4(cidr.strip()),
            connection=ec2.Port.tcp(config.getint(service, 'bolt_port')),
        )
    for cidr in restricted_cidrs:
        NLBSecurityGroup.add_ingress_rule(peer=ec2.Peer.ipv4(cidr.strip()),
            connection=ec2.Port.tcp(config.getint(service, 'http_port')),
        )

    # Attach SG to NLB
    self.NLB.add_security_group(NLBSecurityGroup)

    # Bolt Connection
    ecsService.connections.security_groups[0].add_ingress_rule(
        NLBSecurityGroup,
        ec2.Port.tcp(config.getint(service, 'bolt_port'))
    )

    boltTargetGroup = elbv2.NetworkTargetGroup(self,
        id="nlbTargetGroup",
        target_type=elbv2.TargetType.IP,
        protocol=elbv2.Protocol.TCP,
        port=config.getint(service, 'bolt_port'),
        vpc=self.VPC
    )

    nlbListenerBolt = self.NLB.add_listener("ListenerBolt", port=config.getint(service, 'bolt_port'),)
    nlbListenerBolt.add_target_groups("targetBolt", boltTargetGroup)
    boltTargetGroup.add_target(
        ecsService.load_balancer_target(
            container_name="neo4j",
            container_port=config.getint(service, 'bolt_port')
        )
    )

    # HTTP Connection
    ecsService.connections.security_groups[0].add_ingress_rule(
            NLBSecurityGroup,
            ec2.Port.tcp(config.getint(service, 'http_port'))
        )

    httpTargetGroup = elbv2.NetworkTargetGroup(self,
            id="nlbTargetGroupHttp",
            target_type=elbv2.TargetType.IP,
            protocol=elbv2.Protocol.TCP,
            port=config.getint(service, 'http_port'),
            vpc=self.VPC
        )
    nlbListenerHttp = self.NLB.add_listener("ListenerHttp", port=config.getint(service, 'http_port'),)
    nlbListenerHttp.add_target_groups("targetHttp", httpTargetGroup)
    httpTargetGroup.add_target(
        ecsService.load_balancer_target(
            container_name="neo4j",
            container_port=config.getint(service, 'http_port')
        )
    )

    CfnOutput(self, "Neo4jNlbDnsName",
       value=self.NLB.load_balancer_dns_name,
       export_name="Neo4jNlbDnsNameExport"
    )