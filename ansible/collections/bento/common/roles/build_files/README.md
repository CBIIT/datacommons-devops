build_files
------------

This role builds the Bento Files service container.

Requirements
------------

Requires the community.docker collection to be installed. This role also requires the Trivy vulnerability scanner to be installed in teh environment where it is run.

Role Variables
--------------

Required variables:

ansible_python_interpreter
workspace
build_number
project_name
image_version
container_name
container_build_path
dockerfile_path
container_registry_url

Dependencies
------------

Depends on bento.common.ecr_login to provide ecr_repo variable.

Example Playbook
----------------



License
-------

BSD

Author Information
------------------

Maintained by Bento Devops Team.