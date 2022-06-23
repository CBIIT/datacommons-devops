## Accessing CBIIT's Approved Base Container Images

### Step 1:
Ensure you have Docker and the AWS CLI installed.

### Step 2: 
Retrieve an authentication token and authenticate your Docker client to your registry. Run the following command using the AWS CLI:
<pre><code>aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin {account_id}.dkr.ecr.us-east-1.amazonaws.com</code></pre>
Be sure to replace {account_id} with your AWS account number where you're trying to push images to.

### Step 3: 
Pull the CBIIT-Managed base images by running any of the following docker commands:
<pre><code>docker pull 019211168375.dkr.ecr.us-east-1.amazonaws.com/cbiit-base-docker-images:cbiit-amazon-linux-2
docker pull 019211168375.dkr.ecr.us-east-1.amazonaws.com/cbiit-base-docker-images:cbiit-alpine-linux
docker pull 019211168375.dkr.ecr.us-east-1.amazonaws.com/cbiit-base-docker-images:cbiit-oracle-linux-8
docker pull 019211168375.dkr.ecr.us-east-1.amazonaws.com/cbiit-base-docker-images:cbiit-ubuntu-20.04</code></pre>

