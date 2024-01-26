import argparse
import boto3
import requests
from requests_aws4auth import AWS4Auth
import time

parser = argparse.ArgumentParser(description='Opensearch Backup Script')
parser.add_argument("--oshost", type=str, help="opensearch host with trailing /")
parser.add_argument("--repo", type=str, help="opensearch snapshot repository")
parser.add_argument("--s3bucket", type=str, help="s3 bucket")
parser.add_argument("--snapshot", type=str, help="opensearch snapshot value")
parser.add_argument("--indices", type=str, help="indices")
parser.add_argument("--rolearn", type=str, help="role arn - typically power user role")
parser.add_argument("--basepath", type=str, help="basepath")
args = parser.parse_args()
oshost = args.oshost
repo = args.repo
s3bucket= args.s3bucket
snapshot= args.snapshot 
indices = args.indices
rolearn = args.rolearn 
basepath = args.basepath
# test
host = oshost 
region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

print(awsauth)
path = '_snapshot/'+repo
url = host + path

payload = {
  "type": "s3",
  "settings": {
    "bucket": s3bucket,
    "base_path": basepath,
    "region": "us-east-1",
    "role_arn": rolearn,
    "server_side_encryption": "true"
  }
}

headers = {"Content-Type": "application/json"}
print("registering repo")
r = requests.put(url, auth=awsauth, json=payload, headers=headers)

print(r.status_code)
print(r.text)
time.sleep(100) 

headers = {"Content-Type": "application/json"}
print("starting deleting the indices")
indice_arr = indices.split(",")
for i in indice_arr:
  check = requests.get(oshost+i, auth=awsauth, headers=headers)
  if check.status_code==200:
    r = requests.delete(oshost+i, auth=awsauth, headers=headers)
    print(r.text)

print("finished deleting the indices, waiting 2 mins for the deletion to complete")
time.sleep(120) 
#
print("started restore the indices")
payload_restore = {
  "indices": indices,
  "include_global_state": False
}
path = '_snapshot/'+repo+'/'+snapshot+'/_restore'
print(path)
print(payload)

r = requests.post(oshost+path, auth=awsauth, json=payload_restore, headers=headers)
#
print(r.text)
if r.status_code!=200:
  raise Exception("Sorry, pipeline does not run successfully")