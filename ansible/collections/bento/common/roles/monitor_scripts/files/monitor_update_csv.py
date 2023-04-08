#!/usr/bin/python

import sys, getopt, json, os, csv
from monitors.alerts.policies import set_fargate_policy, set_alb_policy, set_opensearch_policy, set_synthetics_policy
from monitors.synthetics import set_synthetics_monitor
from monitors.alerts.destinations import set_email_destination, set_slack_destination
from monitors.alerts.workflows import set_workflow

def main(input_file):

   #result = setMonitors(input_file)
   result = setSynthetics(input_file)

def setMonitors(input_file):

   with open(input_file, newline='') as csvfile:
     data = csv.DictReader(csvfile)

     tiersSet = []
     for row in data:
       global project
       project = row["Project_Acronym"].upper()
       global tier
       tiers = row["Tiers"].split(',')
       global key
       key = os.getenv('KEY')

       for tier in tiers:
         if project + '-' + tier not in tiersSet:
           print()
           print('Adding Monitor Configuration For: {} {}'.format(project, tier))
           print()

           email_id = set_email_destination.setalertemail("DevOps-FNL", project, tier, key)
           slack_id = set_slack_destination.setalertslack("Expand Data Commons", project, tier, key)
           workflow_id = set_workflow.setalertworkflow(project + "-" + tier + " Notifications", email_id, slack_id, project, tier, key)

           os_policy_id = set_opensearch_policy.setpolicy(project, tier, key)
           alb_policy_id = set_alb_policy.setpolicy(project, tier, key)
           fargate_policy_id = set_fargate_policy.setpolicy(project, tier, key)
           tiersSet.append(project + '-' + tier)
           #print(tiersSet)

   #return(data)

def setSynthetics(input_file):
   with open(input_file, newline='') as csvfile:
     data = csv.DictReader(csvfile)

     tiersSet = []
     for row in data:
       global project
       project = row["Project_Acronym"].upper()
       global tier
       tiers = row["Tiers"].split(',')
       global key
       key = os.getenv('KEY')
       global location
       #location = os.getenv('LOCATION')
       endpoint_name = row["Endpoint_Name"]
       endpoint_url = row["URL"]

       for tier in tiers:
         print()
         print('Adding Synthetics Configuration For: {} {} {}'.format(project, tier, endpoint_name))
         print()

         if project + '-' + tier not in tiersSet:
           synthetics_policy_id = set_synthetics_policy.setpolicy(project, tier, key)
           tiersSet.append(project + '-' + tier)
           #print(tiersSet)
         
         if row["Private_Location"]:
           location = os.getenv('LOCATION')
         else:
           location = 'AWS_US_EAST_1'

         api_data = {}
         api_data['name'] = endpoint_name
         api_data['url'] = endpoint_url
         api = json.loads(json.dumps(api_data))
         api.update({"location": location})
         print('Synthetics Policy:   {}     API:   {}'.format(synthetics_policy_id, api))
         #set_synthetics_monitor.setsyntheticsmonitor(project, tier, key, api, synthetics_policy_id)

   #return(data)

if __name__ == "__main__":
   result = main('FNL-Monitoring-List.csv')