opensearch_dataloading
------------

This role performs two operations:
Opensearch Backup : This task creats OpenSearch snapshot on the lower tier(usually on dev opensearch) and store it in S3 bucket in the prod aws account.

Opensearch restore : This task perform dataloading on the OpenSearch from the snapshot available in S3 bucket in the prod aws account.

Requirements
------------

Role Variables
--------------

Required variables:

For Opensearch Backup:
ansible_python_interpreter
project_name
tier
workspace
region
opensearch_host
snapshot_repo
s3_bucket
snapshot_value
base_path
role_arn

For Opensearch Restore: 
ansible_python_interpreter
project_name
tier
workspace
region
opensearch_host
snapshot_repo
s3_bucket
snapshot_value
base_path
role_arn
indices

Dependencies
------------

Along with the IAM roles(opensearch snapshot role in prod and nonprod account, cross account access role in prod account) created through terraform, we also need to perform additional configurations manually.

we need to enable ACL on the S3 bucket and set Object ownership to Bucket Owner preferred.


Example Playbook
----------------



License
-------

BSD

Author Information
------------------

Maintained by Bento Devops Team.

