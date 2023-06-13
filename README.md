[![Codacy Badge](https://app.codacy.com/project/badge/Grade/2517c2b5f986415b86aa59e2414f4e30)](https://app.codacy.com/gh/CBIIT/datacommons-devops/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

## About
This repository serves as a centralized registry for reusable infrastructure and configuration management definitions to be used across FNL projects. 

## Terraform Module Best Practices & Standards

### Resource Naming Conventions
- Resources should be named using the following convention:
<pre><code> "${stack-name}-${environment}-description"</code></pre>

- The `stack-name` argument is the name of the application
- The `environment` argument is the name of the target tier (consider using `terraform.workspace` in project repositories)
- The `description` argument describes the resource (i.e. "s3-log-bucket" or "opensearch")
- Keep in mind that some resources require globally unique names. Use the `description` argument to ensure global uniqueness when this is the case (S3 buckets, for example)

### IAM Resources
- Creating `IAM Roles` in modules is recommended, but `IAM Policies` attached to these `IAM Roles` should be defined in project repositories.
- For use cases where it makes sense to create `IAM Policies` in a module (i.e. AssumeRole scenarios), use the [IAM Policy Document](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) data source to define the `IAM Policies`.  

### Security Groups
- Creating `Security Groups` in modules is recommended, but `Security Group Rules` attached to these `Security Groups` should be defined in project repositories.

### Folder Structure
- Terraform Modules stored in the `terraform/modules/` directory should have the following folder structure:
<pre><code>
|-- terraform
|   |-- modules
|   |   |-- resource1
|   |   |   |-- data.tf
|   |   |   |-- locals.tf
|   |   |   |-- main.tf
|   |   |   |-- outputs.tf
|   |   |   |-- variables.tf
|   |   |   |-- README.md
|   |   |-- resource2
|   |   |   |-- data.tf
|   |   |   |-- locals.tf
|   |   |   |-- main.tf
|   |   |   |-- outputs.tf
|   |   |   |-- variables.tf
|   |   |   |-- README.md
</code></pre>

## Releases (By Tag Name)
 - v1.5:  
      1. update to the ecs terraform module to fix an error with setting the permissions boundary ARN in upper tier environments.
      2. updated naming as "${var.resource_prefix}-<resource_name/description>" which allows us to provide the resource_prefix at the project level.
 
