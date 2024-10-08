#!/usr/bin/python

import os
import json
import requests
import time
from monitors.alerts.conditions.synthetics import set_synthetics_condition

def setsyntheticsmonitor(project, tier, key, api, policy_id):
   API_ENDPOINT = 'https://api.newrelic.com/graphql'
   NR_ACCT_ID = os.getenv('NR_ACCT_ID')
   monitor_name = '{} {} Certificate Monitor'.format(project, tier)
   location = "public: [\"AWS_US_EAST_1\"]"
   domain = api['url'].replace("https://","")
   domain = domain.replace("/","")
   period = "EVERY_DAY"
   daysToFail = "30"

   monitor_found = False
   headers = {
       "Api-Key": key,
       "Content-Type": "application/json"
   }

   entityQuery = {"query":"{"
     "actor {"
       "entitySearch(query: \"domain = 'SYNTH' AND type = 'MONITOR'\") {"
         "results {"
           "entities {"
             "... on SyntheticMonitorEntityOutline {"
               "name\n"
               "guid\n"
               "monitorID"
             "}"
           "}"
         "}"
       "}"
     "}"
   "}", "variables":""}

   try:
     response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(entityQuery), allow_redirects=False)
     if 'errors' in response.json(): raise ValueError('{} Script Error:   {}'.format(monitor_name, response.json()['errors']))
   except (requests.exceptions.RequestException, ValueError) as e:
     raise SystemExit(e)

   def find_by_key(data, target):
    for key, value in data.items():
        if isinstance(value, dict):
            yield from find_by_key(value, target)
        elif key == target:
            yield value
   
   for x in find_by_key(response.json(), 'entities'):
     entities = x

   for x in entities:
     if monitor_name in x.get("name", "none"):
       monitor_found = True
       monitor_guid = x.get('guid')
       monitor_id = x.get('monitorID')
       print('{} already exists, updating with the latest configuration.'.format(monitor_name))

       data = {"query":"mutation {"
         "syntheticsUpdateCertCheckMonitor ("
           "guid: \"" + monitor_guid + "\","
           "monitor: {"
             "locations: {"
               "" + location + ""
             "},"
             "period: " + period + ","
             "domain: \"" + domain + "\","
             "numberDaysToFailBeforeCertExpires: " + daysToFail + ","
             "status: ENABLED,"
             "runtime: {"
               "runtimeType: \"NODE_API\","
               "runtimeTypeVersion: \"16.10\","
             "},"
             "tags: ["
               "{"
                 "key: \"Project\","
                 "values: [\"" + project + "\"]"
               "},"
               "{"
                 "key: \"Tier\","
                 "values: [\"" + tier + "\"]"
               "},"
             "]"
         "} ) {"
         "errors {"
           "description\n"
           "type"
         "}"
         "}"
       "}", "variables":""}

       try:
         response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data), allow_redirects=False)
         if 'errors' in response.json(): raise ValueError('{} Script Error:   {}'.format(monitor_name, response.json()['errors']))
       except (requests.exceptions.RequestException, ValueError) as e:
         raise SystemExit(e)

   if not monitor_found:
     data = {"query":"mutation {"
       "syntheticsCreateCertCheckMonitor("
         "accountId: " + NR_ACCT_ID + ","
         "monitor: {"
           "locations: {"
             "" + location + ""
           "},"
           "name: \"" + monitor_name + "\","
           "period: " + period + ","
           "domain: \"" + domain + "\","
           "numberDaysToFailBeforeCertExpires: " + daysToFail + ","
           "status: ENABLED,"
           "runtime: {"
             "runtimeType: \"NODE_API\","
             "runtimeTypeVersion: \"16.10\","
           "},"
           "tags: ["
             "{"
               "key: \"Project\","
               "values: [\"" + project + "\"]"
             "},"
             "{"
               "key: \"Tier\","
               "values: [\"" + tier + "\"]"
             "},"
           "]"
         "} ) {"
         "errors {"
           "description\n"
           "type"
         "}"
         "}"
       "}", "variables":""}

     try:
       response = requests.post('{}'.format(API_ENDPOINT), headers=headers, data=json.dumps(data), allow_redirects=False)
       if 'errors' in response.json(): raise ValueError('{} Script Error:   {}'.format(monitor_name, response.json()['errors']))
     except (requests.exceptions.RequestException, ValueError) as e:
       raise SystemExit(e)
     print("{} was created".format(monitor_name))
     
     # get the newly created monitor
     # pause to allow it to be created
     time.sleep(15)
     try:
       response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(entityQuery), allow_redirects=False)
       if 'errors' in response.json(): raise ValueError('{} Script Error:   {}'.format(monitor_name, response.json()['errors']))
     except (requests.exceptions.RequestException, ValueError) as e:
       raise SystemExit(e)
   
     for x in find_by_key(response.json(), 'entities'):
       entities = x

     for x in entities:
       if monitor_name in x.get("name", "none"):
         monitor_id = x.get('monitorID')
     
   # add synthetics condition
   set_synthetics_condition.setcondition(project, tier, key, 'Cert', monitor_id, policy_id)