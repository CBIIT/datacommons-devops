import argparse
import boto3
import requests
from requests_aws4auth import AWS4Auth
import time

def getArgs():

  parser = argparse.ArgumentParser(description='Opensearch Backup Script')
  parser.add_argument("--oshost", type=str, help="opensearch host with trailing /")
  parser.add_argument("--repo", type=str, help="opensearch snapshot repository")
  parser.add_argument("--s3bucket", type=str, help="s3 bucket")
  parser.add_argument("--snapshot", type=str, help="opensearch snapshot value")
  parser.add_argument("--indices", type=str, help="indices", nargs='?', const='')
  parser.add_argument("--rolearn", type=str, help="role arn - typically power user role")
  parser.add_argument("--basepath", type=str, help="basepath", nargs='?', const='')
  parser.add_argument("--region", type=str, help="region")
  args = parser.parse_args()
  
  argList = {}
  argList['oshost'] = args.oshost
  argList['repo'] = args.repo
  argList['s3bucket'] = args.s3bucket
  argList['snapshot'] = args.snapshot 
  argList['indices'] = args.indices
  argList['rolearn'] = args.rolearn
  argList['region'] = args.region

  basepath = args.basepath
  if basepath :
    argList['basepath'] = basepath + '/' + argList['snapshot']
  else:
    argList['basepath'] = argList['snapshot']

  return argList


def osAuth(argList):
  # Opensearch authentication
  service = 'es'
  credentials = boto3.Session().get_credentials()
  awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, argList['region'], service, session_token=credentials.token)
  print(awsauth)

  return awsauth


def registerRepo(argList, awsauth):

  # Registering Repo
  path = '_snapshot/' + argList['repo']
  url = argList['oshost'] + path

  payload = {
    "type": "s3",
    "settings": {
      "bucket": argList['s3bucket'],
      "base_path": argList['basepath'],
      "region": argList['region'],
      "role_arn": argList['rolearn'],
      "canned_acl": "bucket-owner-full-control"
    }
  }

  headers = {"Content-Type": "application/json"}
  print("registering repo")
  try:
    r = requests.put(url, auth=awsauth, json=payload, headers=headers)
    print(r.status_code)
    print(r.text)
    time.sleep(100)
  except requests.exceptions.RequestException as e:
    raise SystemExit(e)


def deleteIndexes(argList, awsauth):
  # Deleting Indexes
  headers = {"Content-Type": "application/json"}
  
  if argList['indices']:
    print("deleting the listed indices")
    indice_arr = argList['indices'].split(",")
    for i in indice_arr:
      check = requests.get(argList['oshost'] + i, auth=awsauth, headers=headers)
      if check.status_code==200:
        try:
          r = requests.delete(argList['oshost'] + i, auth=awsauth, headers=headers)
          print(r.text)
        except requests.exceptions.RequestException as e:
          raise SystemExit(e)
  else:
    print("no listed indices - deleting all indices")
    try:
      r = requests.delete(argList['oshost'] + '/*', auth=awsauth, headers=headers)
      print(r.text)
    except requests.exceptions.RequestException as e:
     raise SystemExit(e)

  print("finished deleting the indices, waiting 2 mins for the deletion to complete")
  time.sleep(120)


def restoreIndexes(argList, awsauth):

  # Restoring Indexes
  print("started restore the indices")
  
  headers = {"Content-Type": "application/json"}
  payload = {
    "indices": argList['indices'],
    "include_global_state": False,
    "rename_pattern": ".kibana*",
    "rename_replacement": "restored_.kibana*"
  }
  path = '_snapshot/' + argList['repo'] + '/' + argList['snapshot'] + '/_restore'
  print(path)

  try:
    result = requests.post(argList['oshost'] + path, auth=awsauth, json=payload, headers=headers)
  except requests.exceptions.RequestException as e:
     raise SystemExit(e)
  else:
    # reindex restored_.kibana to .kibana 
    payload = {
      "source": {
        "index": "restored_.kibana"
      },
      "dest": {
        "index": ".kibana"
      }
    }
    try:
      result = requests.post(argList['oshost'] + '_reindex', auth=awsauth, json=payload, headers=headers)
    except requests.exceptions.RequestException as e:
      raise SystemExit(e)

  return result


if __name__ == "__main__":
   argList = getArgs()
   awsauth = osAuth(argList)
   registerRepo(argList, awsauth)

   deleteIndexes(argList, awsauth)
   result = restoreIndexes(argList, awsauth)
   print(result.text)
   if result.status_code!=200:
    raise Exception("Sorry, pipeline does not run successfully")