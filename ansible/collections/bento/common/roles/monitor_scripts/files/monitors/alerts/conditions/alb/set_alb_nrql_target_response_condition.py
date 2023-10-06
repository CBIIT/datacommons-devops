#!/usr/bin/python

import json
import requests
from tags import set_tags_nrql

def setcondition(key, project, tier, policy_id):

   ####################     Condition Specific Variables          ####################

   condition_name = '{} {} ALB Target Response Time'.format(project, tier)
   query = "FROM Metric SELECT average(`aws.applicationelb.TargetResponseTime`) WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ApplicationELB' AND entity.name LIKE '%{}-{}-lb%'"
   critical_duration = "1"
   critical_threshold = "0.4"
   warning_duration = "1"
   warning_threshold = "0.2"

   ###################################################################################

   API_ENDPOINT = 'https://api.newrelic.com/v2/alerts_nrql_conditions.json'
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
         "duration" : critical_duration,
         "operator" : "above",
         "threshold" : critical_threshold,
         "time_function" : "all",
         "priority" : "critical"
       }, {
         "duration" : warning_duration,
         "operator" : "above",
         "threshold" : warning_threshold,
         "time_function" : "all",
         "priority" : "warning"
       } ],
       "value_function" : "single_value",
       "nrql" : {
         "query" : query.format(project.lower(), tier.lower())
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