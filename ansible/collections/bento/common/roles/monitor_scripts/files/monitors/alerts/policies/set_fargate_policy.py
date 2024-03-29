#!/usr/bin/python

import os
import json
import requests
from monitors.alerts.conditions.fargate import set_fargate_nrql_cpu_condition, set_fargate_nrql_mem_condition, set_fargate_nrql_restarts_condition

def setpolicy(project, tier, key, policyList):

   policy_name = '{} {} Fargate Policy'.format(project, tier)
   policy_found = False

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

   for x in policyList:
     if policy_name in x.get("name", "none"):
       policy_found = True
       policy_id = x.get("id", "none")

   if not policy_found:

     API_ENDPOINT = 'https://api.newrelic.com/v2/alerts_policies.json'

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
     
   # add fargate CPU condition
   set_fargate_nrql_cpu_condition.setcondition(key, project, tier, policy_id)

   # add fargate Memory condition
   set_fargate_nrql_mem_condition.setcondition(key, project, tier, policy_id)

   # add fargate Restarts condition
   set_fargate_nrql_restarts_condition.setcondition(key, project, tier, policy_id)
   
   return(policy_id)