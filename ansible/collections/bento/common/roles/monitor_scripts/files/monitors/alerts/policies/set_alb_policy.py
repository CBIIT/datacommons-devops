#!/usr/bin/python

import os
import json
import requests
from monitors.alerts.conditions.alb import set_alb_nrql_elb_4xx_condition, set_alb_nrql_elb_5xx_condition, set_alb_nrql_target_5xx_condition, set_alb_nrql_target_response_condition, set_alb_nrql_tls_condition, set_alb_nrql_unhealthy_host_condition

def setpolicy(project, tier, key):
   API_ENDPOINT = 'https://api.newrelic.com/graphql'
   NR_ACCT_ID = os.getenv('NR_ACCT_ID')

   policy_name = '{} {} ALB Policy'.format(project, tier)
   policy_found = False

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

   for x in response.json()['data']['actor']['account']['alerts']['policiesSearch']['policies']:
     if policy_name in x.get("name", "none"):
       policy_found = True
       policy_id = x.get("id", "none")

   headers = {
     "Api-Key": key,
     "Content-Type": "application/json"
   }
   
   data = {
     "policy": {
       "incident_preference": "PER_POLICY",
       "name": policy_name
     }
   }

   if not policy_found:

     API_ENDPOINT = 'https://api.newrelic.com/v2/alerts_policies.json'

     headers = {
       "Api-Key": key,
       "Content-Type": "application/json"
     }

     data = {
       "policy": {
         "incident_preference": "PER_POLICY",
         "name": policy_name
       }
     }

     # create policy
     try:
       response = requests.post('{}'.format(API_ENDPOINT), headers=headers, data=json.dumps(data), allow_redirects=False)
     except requests.exceptions.RequestException as e:
       raise SystemExit(e)
     policy_id = response.json()['policy'].get("id", "none")

     try:
       response = requests.put('https://api.newrelic.com/v2/alerts_policy_channels.json', headers=headers, data=json.dumps(data), allow_redirects=False)
     except requests.exceptions.RequestException as e:
       raise SystemExit(e)
     print('{} Created'.format(policy_name))

   else:
     print('{} already exists - updating with the latest configuration'.format(policy_name))

     API_ENDPOINT = 'https://api.newrelic.com/v2/alerts_policies/{}.json'.format(policy_id)

     # update policy
     try:
       response = requests.put('{}'.format(API_ENDPOINT), headers=headers, data=json.dumps(data), allow_redirects=False)
     except requests.exceptions.RequestException as e:
       raise SystemExit(e)
     
   # add alb elb 4xx condition
   set_alb_nrql_elb_4xx_condition.setcondition(key, project, tier, policy_id)

   # add alb elb 5xx condition
   set_alb_nrql_elb_5xx_condition.setcondition(key, project, tier, policy_id)

   # add alb target 5xx condition
   set_alb_nrql_target_5xx_condition.setcondition(key, project, tier, policy_id)

   # add alb target response condition
   set_alb_nrql_target_response_condition.setcondition(key, project, tier, policy_id)
   
   # add alb tls condition
   set_alb_nrql_tls_condition.setcondition(key, project, tier, policy_id)

   # add alb unhealthy host condition
   set_alb_nrql_unhealthy_host_condition.setcondition(key, project, tier, policy_id)

   return(policy_id)