#!/usr/bin/python

import sys, getopt
from monitors.alerts.policies import set_fargate_policy
from monitors.synthetics import set_synthetics_monitor
from monitors.alerts.destinations import set_email_destination, set_slack_destination
from monitors.alerts.workflows import set_workflow

def main(argv):

   global project
   project = ''
   global tier
   tier = ''
   global key
   key = ''
   global auth
   auth = ''
   try:
      opts, args = getopt.getopt(argv,"hp:t:k:a:",["project=","tier=","key=","auth="])
   except getopt.GetoptError:
      print('monitor_query.py -p <project> -t <tier> -k <newrelic api key> -a <sumologic basic auth>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('monitor_query.py -p <project> -t <tier> -k <api key>')
         sys.exit()
      elif opt in ("-p", "--project"):
         project = arg
      elif opt in ("-t", "--tier"):
         tier = arg
      elif opt in ("-k", "--key"):
         key = arg
      elif opt in ("-a", "--auth"):
         auth = arg

if __name__ == "__main__":
   main(sys.argv[1:])

   print()
   print('Adding Monitor Configuration For: {} {}'.format(project, tier))
   print()

   email_id = set_email_destination.setalertemail("DevOps-FNL", project, tier, key)
   slack_id = set_slack_destination.setalertslack("Expand Data Commons", project, tier, key)
   workflow_id = set_workflow.setalertworkflow(project.capitalize() + "-" + tier.capitalize() + " Notifications", email_id, slack_id, project, tier, key)

   fargate_policy_id = set_fargate_policy.setfargatealertpolicy(project, tier, key)
   
   synthetics_location = '2292606-leidos_cloud-DFA'
   
   if tier == 'prod':
     url_location = 'AWS_US_EAST_1'
   else:
     url_location = synthetics_location
   
   apiList = [
     {'name':'url','endpoint':'','location':url_location},
     {'name':'files','endpoint':'/files','location':synthetics_location}
   ]
   
   for api in apiList:
     set_synthetics_monitor.setsyntheticsmonitor(project, tier, key, api, fargate_policy_id)