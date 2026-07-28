#!/usr/bin/env python3
import os, sys
import logging
import aws_cdk as cdk

from configparser import ConfigParser, ExtendedInterpolation
from aws_cdk import aws_iam as iam

from app.stack import Stack
from app.aspects import MyAspect

# Read config
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read("config.ini")

if __name__=="__main__":
  logging.basicConfig(format='%(asctime)s [%(levelname)5s] %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S',
                        level=logging.NOTSET)

  if config.has_option('iam', 'role_prefix'):
    synthesizer = cdk.DefaultStackSynthesizer(
        # ARN of the role assumed by the CLI and Pipeline to deploy here
        deploy_role_arn="arn:${AWS::Partition}:iam::${AWS::AccountId}:role/" + config['iam']['role_prefix'] + "-cdk-${Qualifier}-deploy-role-${AWS::Region}",

        # ARN of the role used for file asset publishing (assumed from the CLI role)
        file_asset_publishing_role_arn="arn:${AWS::Partition}:iam::${AWS::AccountId}:role/" + config['iam']['role_prefix'] + "-cdk-${Qualifier}-file-publishing-role-${AWS::Region}",

        # ARN of the role used for Docker asset publishing (assumed from the CLI role)
        image_asset_publishing_role_arn="arn:${AWS::Partition}:iam::${AWS::AccountId}:role/" + config['iam']['role_prefix'] + "-cdk-${Qualifier}-image-publishing-role-${AWS::Region}",

        # ARN of the role passed to CloudFormation to execute the deployments
        cloud_formation_execution_role="arn:${AWS::Partition}:iam::${AWS::AccountId}:role/" + config['iam']['role_prefix'] + "-cdk-${Qualifier}-cfn-exec-role-${AWS::Region}",

        # ARN of the role used to look up context information in an environment
        lookup_role_arn="arn:${AWS::Partition}:iam::${AWS::AccountId}:role/" + config['iam']['role_prefix'] + "-cdk-${Qualifier}-lookup-role-${AWS::Region}",
      )
  else:
    synthesizer = cdk.DefaultStackSynthesizer()
  
  app = cdk.App()

  stack_name="{}-{}".format(config['main']['resource_prefix'], config['main']['tier'])
  stack = Stack(
    app,
    stack_name,
    synthesizer=synthesizer,
    env=cdk.Environment(
      account=config['main']['account_id'],
      region=config['main']['region']
    ),
  ) 

  # Rename all roles to add role prefix
  cdk.Aspects.of(stack).add(MyAspect())

  # set permission boundary on all roles
  if config.has_option('iam', 'permission_boundary'):
    boundary = iam.ManagedPolicy.from_managed_policy_arn(stack, "Boundary", config['iam']['permission_boundary'])
    iam.PermissionsBoundary.of(stack).apply(boundary)

  config_tags = dict(s.split(':') for s in config['main']['tags'].split(","))
  env_tags = {'Environment': config['main']['tier']}
  tags = config_tags | env_tags


  for tag,value in tags.items():
    cdk.Tags.of(stack).add(tag, value)

  app.synth()
