import requests
import os
import re
import sys
import json

# Set constants
GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
GITHUB_BASE_URL = 'https://api.github.com'
ORG_NAME = 'CBIIT'
IMAGE_TAG = 'fnl_base_image'


def getRepos(orgName):

  organization_repositories_url = f"{GITHUB_BASE_URL}/orgs/{orgName}/repos"

  query_url = f"{organization_repositories_url}?simple=yes&per_page=100&page=1"


  headers = {'Authorization': 'token ' + GITHUB_ACCESS_TOKEN}

  res=requests.get(query_url,headers=headers)
  repos=res.json()

  while 'next' in res.links.keys():
    res=requests.get(res.links['next']['url'],headers=headers)
    repos.extend(res.json())
  
  return repos


def getBranches(orgName, repo):

  branches_url = f"{GITHUB_BASE_URL}/repos/{orgName}/{repo}/branches"
  
  headers = {'Authorization': 'token ' + GITHUB_ACCESS_TOKEN}

  res=requests.get(branches_url,headers=headers)
  branches=res.json()
  
  return branches


def getFiles(orgName, repo, branch):
  
  tree_url = f"{GITHUB_BASE_URL}/repos/{orgName}/{repo}/git/trees/{branch}?recursive=1"
  
  headers = {'Authorization': 'token ' + GITHUB_ACCESS_TOKEN}
  res=requests.get(tree_url,headers=headers)
  files_dict=res.json()

  repo_images = []
  if 'tree' in files_dict:
    for f in files_dict['tree']:
      if 'dockerfile' in f['path'].lower():
        image = getImages(orgName, repo, branch, f['path'])
        if image:
          #print(f"Image is:     {image}")
          image_dict = {"Name":image, "Projects":f"{repo}:{branch}"}
          #print(f"Image dict is:     {image_dict}")
          repo_images.append(image_dict)

  return repo_images


def getImages(orgName, repo, branch, file):
  
  raw_url =  f"https://raw.githubusercontent.com/{orgName}/{repo}/{branch}/{file}"
  headers = {'Authorization': 'token ' + GITHUB_ACCESS_TOKEN}

  res=requests.get(raw_url,headers=headers)

  image = re.search('from (.*) as fnl_base_image', res.text, re.IGNORECASE)
  if image:
    return image.group(1)


if __name__ == "__main__":
  image_list = []
  repos = getRepos(ORG_NAME)
  #print(f"Number of Repos Found:   {len(repos)}")
  num_repos = len(repos)

  for r in repos:
    branch_list = getBranches(ORG_NAME, r['name'])
    for b in branch_list:
      repo_images = getFiles(ORG_NAME, r['name'], b['name'])
      image_list.extend(repo_images)

  #print(f"Image List: {image_list}")

  count = '{ "repo_count": "' + str(num_repos) + '"}'
  result = json.loads(count)

  images = json.dumps({'images': image_list})
  loaded_images = json.loads(images)

  result.update(loaded_images)
  #print(f"Results: {result}")
  sys.stdout.write(str(result))
  sys.stdout.flush()
  sys.exit(0)
