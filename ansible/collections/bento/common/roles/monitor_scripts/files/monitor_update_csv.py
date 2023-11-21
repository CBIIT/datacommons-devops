#!/usr/bin/python

import sys, getopt, json, os, csv, codecs, requests, contextlib
from monitors.alerts.policies import set_fargate_policy, set_alb_policy, set_opensearch_policy, set_synthetics_policy
from monitors.synthetics import set_synthetics_monitor_simple_browser, set_synthetics_monitor_scripted_api
from monitors.alerts.destinations import set_email_destination, set_slack_destination
from monitors.alerts.workflows import set_workflow

def main(argv):

   try:
      opts, args = getopt.getopt(argv,"hf:",["file="])
   except getopt.GetoptError:
      print('File URL Required:   monitor_update_csv.py -f <file>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('monitor_update_csv.py -f <file>')
         sys.exit()
      elif opt in ("-f", "--file"):
         input_url = arg

   policyList = getpolicylist(os.getenv('KEY'))
   print(policyList)

   result = setMonitors(input_url, policyList)
   result = setSynthetics(input_url, policyList)

def getpolicylist(key):
   API_ENDPOINT = 'https://api.newrelic.com/graphql'
   NR_ACCT_ID = os.getenv('NR_ACCT_ID')

   headers = {
     "Api-Key": key,
     "Content-Type": "application/json"
   }
   
   data = """{{
     actor {{
       account(id: {}) {{
         alerts {{
           policiesSearch {{
             policies {{
               name
               id
             }}
           }}
         }}
       }}
     }}
   }}""".format(NR_ACCT_ID)

   payload = { "query": data }

   try:
     response = requests.post('{}'.format(API_ENDPOINT), headers=headers, data=json.dumps(payload), allow_redirects=False)
   except requests.exceptions.RequestException as e:
     raise SystemExit(e)

   return(response.json()['data']['actor']['account']['alerts']['policiesSearch']['policies'])

def setMonitors(input_url, policyList):

   with contextlib.closing(requests.get(input_url, stream=True)) as csvfile:
     data = csv.DictReader(codecs.iterdecode(csvfile.iter_lines(), 'utf-8'))

     tiersSet = []
     for row in data:
       global project
       project = row["Project_Acronym"].upper()
       global tier
       tier = row["Tier"]
       global key
       key = os.getenv('KEY')
       slack_channel = row["Slack_Channel"]
       resources = row["Monitored_Resources"].split(",")

       if project + '-' + tier not in tiersSet:
         print()
         print('Adding Monitor Configuration For: {} {}'.format(project, tier))
         print()

         email_id = set_email_destination.setalertemail("DevOps-FNL", project, tier, key)
         slack_id = set_slack_destination.setalertslack("Expand Data Commons", project, tier, key, slack_channel)
         workflow_id = set_workflow.setalertworkflow(project + "-" + tier + " Notifications", email_id, slack_id, project, tier, key)

         if 'opensearch' in resources:
           print('adding opensearch config')
           os_policy_id = set_opensearch_policy.setpolicy(project, tier, key, policyList)
         if 'alb' in resources:
           print('adding alb config')
           alb_policy_id = set_alb_policy.setpolicy(project, tier, key, policyList)
         if 'fargate' in resources:
           print('adding fargate config')
           fargate_policy_id = set_fargate_policy.setpolicy(project, tier, key, policyList)
         tiersSet.append(project + '-' + tier)

def setSynthetics(input_url, policyList):

   with contextlib.closing(requests.get(input_url, stream=True)) as csvfile:
     data = csv.DictReader(codecs.iterdecode(csvfile.iter_lines(), 'utf-8'))

     tiersSet = []
     for row in data:
       global project
       project = row["Project_Acronym"].upper()
       global tier
       tier = row["Tier"]
       global key
       key = os.getenv('KEY')
       global location
       endpoint_name = row["Endpoint_Name"]
       monitor_url = row["URL"]

       print()
       print('Adding Synthetics Configuration For: {} {} {}'.format(project, tier, endpoint_name))
       print()

       if project + '-' + tier not in tiersSet:
         synthetics_policy_id = set_synthetics_policy.setpolicy(project, tier, key, policyList)
         tiersSet.append(project + '-' + tier)

       api_data = {}
       api_data['name'] = endpoint_name
       api_data['url'] = monitor_url
       api = json.loads(json.dumps(api_data))
       api.update({"location": row["Private_Location"]})
       api.update({"query": row["Endpoint_Query"]})

       if api['query']:
         set_synthetics_monitor_scripted_api.setsyntheticsmonitor(project, tier, key, api, synthetics_policy_id)
       else:
         set_synthetics_monitor_simple_browser.setsyntheticsmonitor(project, tier, key, api, synthetics_policy_id)


if __name__ == "__main__":
   result = main(sys.argv[1:])