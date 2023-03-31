#!/usr/bin/python

import os
import json
import requests
from monitors.alerts.conditions.os import set_os_nrql_5xx_condition, set_os_nrql_cluster_red_condition, set_os_nrql_cluster_yellow_condition, set_os_nrql_cpu_condition, set_os_nrql_disk_throttle_condition, set_os_nrql_jvm_memory_condition, set_os_nrql_master_cpu_condition, set_os_nrql_master_jvm_memory_condition, set_os_nrql_master_sys_memory_condition, set_os_nrql_search_queue_condition, set_os_nrql_storage_condition, set_os_nrql_sys_memory_condition

def setpolicy(project, tier, key):
   API_ENDPOINT = 'https://api.newrelic.com/v2/alerts_policies.json'

   policy_name = '{}-{} Opensearch Policy'.format(project.title(), tier.title())
   policy_found = False
   headers = {'Api-Key': key}
   
   try:
     response = requests.get('{}'.format(API_ENDPOINT), headers=headers)
   except requests.exceptions.RequestException as e:
     raise SystemExit(e)

   for x in response.json()['policies']:
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
     
   # add conditions
   set_os_nrql_5xx_condition.setcondition(key, project, tier, policy_id)
   set_os_nrql_cluster_red_condition.setcondition(key, project, tier, policy_id)
   set_os_nrql_cluster_yellow_condition.setcondition(key, project, tier, policy_id)
   set_os_nrql_cpu_condition.setcondition(key, project, tier, policy_id)
   set_os_nrql_disk_throttle_condition.setcondition(key, project, tier, policy_id)
   set_os_nrql_jvm_memory_condition.setcondition(key, project, tier, policy_id)
   set_os_nrql_master_cpu_condition.setcondition(key, project, tier, policy_id)
   set_os_nrql_master_jvm_memory_condition.setcondition(key, project, tier, policy_id)
   set_os_nrql_master_sys_memory_condition.setcondition(key, project, tier, policy_id)
   set_os_nrql_search_queue_condition.setcondition(key, project, tier, policy_id)
   set_os_nrql_storage_condition.setcondition(key, project, tier, policy_id)
   set_os_nrql_sys_memory_condition.setcondition(key, project, tier, policy_id)

   return(policy_id)