#!/usr/bin/python

import json
import requests
from tags import set_tags_nrql

def setcondition(key, project, tier, policy_id):

   API_ENDPOINT = 'https://api.newrelic.com/v2/alerts_nrql_conditions.json'

   condition_name = '{}-{} Opensearch Master JVM Memory'.format(project, tier)
   condition_found = False
   headers = {'Api-Key': key}
   data = {'policy_id': policy_id}

   try:
     response = requests.get('{}'.format(API_ENDPOINT), headers=headers, data=data, allow_redirects=False)
   except requests.exceptions.RequestException as e:
     raise SystemExit(e)

   for x in response.json()['nrql_conditions']:
     if condition_name in x.get("name", "none"):
       condition_found = True
       condition_id = x.get("id", "none")

   host_query = "(label.Project = '{}' AND label.Environment = '{}')".format(project, tier)

   headers = {
       "Api-Key": key,
       "Content-Type": "application/json"
   }

   data = {
     "nrql_condition" : {
       "type" : "static",
       "name" : "{}".format(condition_name),
       "enabled" : True,
       "terms" : [ {
         "duration" : "5",
         "operator" : "above",
         "threshold" : "80",
         "time_function" : "all",
         "priority" : "critical"
       }, {
         "duration" : "2",
         "operator" : "above",
         "threshold" : "80",
         "time_function" : "all",
         "priority" : "warning"
       } ],
       "value_function" : "single_value",
       "nrql" : {
         "query" : "FROM  Metric SELECT average(`aws.es.MasterJVMMemoryPressure`) WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND entity.name = '{}-{}-opensearch'".format(project.lower(), tier.lower())
       },
       "signal" : {
         "aggregation_window" : "60",
         "aggregation_method" : "EVENT_FLOW",
         "aggregation_delay" : 120,
         "fill_option" : "none"
       }
     }
   }

   if not condition_found:
     # create condition
     API_ENDPOINT = 'https://api.newrelic.com/v2/alerts_nrql_conditions/policies/{}.json'.format(policy_id)

     try:
       response = requests.post('{}'.format(API_ENDPOINT), headers=headers, data='{}'.format(json.dumps(data)), allow_redirects=False)
     except requests.exceptions.RequestException as e:
       raise SystemExit(e)
     print('{} Created'.format(condition_name))

   else:
     print('{} already exists - updating with the latest configuration'.format(condition_name))

     API_ENDPOINT = 'https://api.newrelic.com/v2/alerts_nrql_conditions/{}.json'.format(condition_id)

     # update condition
     try:
       response = requests.put('{}'.format(API_ENDPOINT), headers=headers, data='{}'.format(json.dumps(data)), allow_redirects=False)
     except requests.exceptions.RequestException as e:
       raise SystemExit(e)

   # set tags on the monitor
   #set_tags_nrql.settagsnrql(project, tier, condition_name, key)