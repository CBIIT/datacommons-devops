### To use this dockerfile copy it to an EC2 instance with access to the bucket you will need to mount and run the following command to start and run the container:
###    docker run --rm -it --privileged $(docker build -q .)
###
### Once inside the container mount your bucket using the command:
###    mkdir < bucket name > && < bucket name > < bucket name >

FROM amazonlinux:2023

RUN yum update -y && yum install -y wget

RUN wget https://s3.amazonaws.com/mountpoint-s3-release/latest/x86_64/mount-s3.rpm \
   && yum install -y ./mount-s3.rpm