- It's okay to create IAM ROLES in modules, but leave IAM POLICY definitions for project repos
- It's okay to create SECURITY GROUPS in modules, but leave SECURITY GROUP RULES for project repos
- Name resources defined in modules using the following format: "{stack-name}-{tier/env}-{resource-descriptor}

## About
This repository serves as a centralized registry for reusable infrastructure and configuration management definitions to be used across FNL projects. 

## Repository Structure

## How to Contribute

## Terraform Module Best Practices

### IAM Resources
- Creating roles in modules is recommended, but policies attached to IAM Roles should be defined in project repositories. For use cases where it makes sense to create IAM Policies in a module (i.e. AssumeRole scenarios), use the [IAM Policy Document](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) data source to define the Policies.  

### Folder Structure
- Each module directory should be structured with main.tf, variables.tf, outputs.tf, locals.tf, data.tf and a README.md file
