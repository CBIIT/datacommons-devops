import argparse
import boto3
import requests
from requests_aws4auth import AWS4Auth

parser = argparse.ArgumentParser(description='Opensearch Backup Script')
parser.add_argument("--oshost", type=str, help="opensearch host with trailing /")
parser.add_argument("--repo", type=str, help="opensearch snapshot repository")
parser.add_argument("--s3bucket", type=str, help="s3 bucket")
parser.add_argument("--basePath", type=str, help="s3 bucket base path", default="")
parser.add_argument("--snapshot", type=str, help="opensearch snapshot value")
parser.add_argument("--region", type=str, help="region")
parser.add_argument("--rolearn", type=str, help="role arn - typically power user role")
args = parser.parse_args()
print(args)
oshost = args.oshost
repo = args.repo

s3bucket= args.s3bucket
snapshot= args.snapshot 
rolearn= args.rolearn

#basepath= args.basePath
if args.basepath :
  basepath = args.basepath + '/'
else:
  basepath = ''

host = (oshost) 
region = args.region
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Register repository
headers = {"Content-Type": "application/json"}
path = '_snapshot/'+repo
url = host + path
payload = {
  "type": "s3",
  "settings": {
    "bucket": s3bucket,
    "base_path": basepath+snapshot,
    "region": region,
    "role_arn": rolearn,
    "canned_acl": "bucket-owner-full-control"
  }
}

#create repo if not present
print(payload)
print("check repo")
# r_get_repo = requests.get(url, auth=awsauth, json=payload, headers=headers)
# if(r_get_repo.status_code!=200):
#   print("repo does not exist, creating it")
#   r_create_repo= requests.put(url, auth=awsauth, json=payload, headers=headers)
#   print(r_create_repo.status_code)
#   print(r_create_repo.text)

# print(r_get_repo.status_code)
# print(r_get_repo.text)

r_create_repo= requests.put(url, auth=awsauth, json=payload, headers=headers)

#snapshot
snapshot_path = '_snapshot/' + repo+'/' + snapshot+'/'
print(snapshot_path) 
url_create_snapshot = host + snapshot_path
payload = {
  "type": "s3",
  "settings": {
    "bucket": s3bucket,
    "base_path": basepath+snapshot,
    "region": region,
    "role_arn": rolearn,
    "canned_acl": "bucket-owner-full-control"
  }
}


print("taking opensearch snapshot")
r = requests.put(url_create_snapshot, auth=awsauth, json=payload, headers=headers)

print(r.status_code)
print(r.text)
if r.status_code!=200:
  raise Exception("Sorry, pipeline does not run successfully")
