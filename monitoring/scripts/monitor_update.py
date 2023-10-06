#!/usr/bin/python

import sys, getopt, json
from monitors.alerts.policies import set_fargate_policy, set_alb_policy, set_opensearch_policy, set_synthetics_policy
from monitors.synthetics import set_synthetics_monitor
from monitors.alerts.destinations import set_email_destination, set_slack_destination
from monitors.alerts.workflows import set_workflow

def main(argv):

   global project
   project = ''
   global tier
   tier = ''
   global services
   services = []
   global key
   key = ''
   global location
   location = ''
   try:
      opts, args = getopt.getopt(argv,"hp:t:s:k:l:",["project=","tier=","services=","key=","location="])
   except getopt.GetoptError:
      print('monitor_query.py -p <project> -t <tier> -s <collection of service configurations> -k <newrelic api key> -l <newrelic location id>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('monitor_query.py -p <project> -t <tier> -s <collection of service configurations> -k <newrelic api key> -l <newrelic location id>')
         sys.exit()
      elif opt in ("-p", "--project"):
         project = arg.upper()
      elif opt in ("-t", "--tier"):
         tier = arg.capitalize()
      elif opt in ("-s", "--services"):
         services = arg.split('|')
      elif opt in ("-k", "--key"):
         key = arg
      elif opt in ("-l", "--location"):
         location = arg

if __name__ == "__main__":
   main(sys.argv[1:])

   if tier == 'Qa':
     tier = 'QA'

   print()
   print('Adding Monitor Configuration For: {} {}'.format(project, tier))
   print()

   email_id = set_email_destination.setalertemail("DevOps-FNL", project, tier, key)
   slack_id = set_slack_destination.setalertslack("Expand Data Commons", project, tier, key)
   workflow_id = set_workflow.setalertworkflow(project + "-" + tier + " Notifications", email_id, slack_id, project, tier, key)

   os_policy_id = set_opensearch_policy.setpolicy(project, tier, key)
   alb_policy_id = set_alb_policy.setpolicy(project, tier, key)
   fargate_policy_id = set_fargate_policy.setpolicy(project, tier, key)
   synthetics_policy_id = set_synthetics_policy.setpolicy(project, tier, key)

   if location:
     syn_location = location
   else:
     syn_location = 'AWS_US_EAST_1'

   for service_config in services:
     api = json.loads(service_config)
     api.update({"location": syn_location})
     set_synthetics_monitor.setsyntheticsmonitor(project, tier, key, api, synthetics_policy_id)