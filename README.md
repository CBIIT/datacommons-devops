## About
This repository serves as a centralized registry for reusable infrastructure and configuration management definitions to be used across FNL projects. 

## Repository Structure

## How to Contribute

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
- Each module directory should be structured with main.tf, variables.tf, outputs.tf, locals.tf, data.tf and a README.md file
