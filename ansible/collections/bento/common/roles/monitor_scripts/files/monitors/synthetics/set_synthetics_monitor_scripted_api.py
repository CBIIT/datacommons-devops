#!/usr/bin/python

import os
import json
import requests

def setsyntheticsmonitor(project, tier, key, api, policy_id):
   API_ENDPOINT = 'https://api.newrelic.com/graphql'
   NR_ACCT_ID = os.getenv('NR_ACCT_ID')
   monitor_name = '{} {} {} Monitor'.format(project, tier, api['name'])

   if tier.lower() == 'prod':
     freq = 'EVERY_10_MINUTES'
   else:
     freq = 'EVERY_30_MINUTES'

   if api['location'] and tier.lower() != 'prod':
     location = '''private: {{
       guid: "{guid}",
       vsePassword: "{password}"
       }}'''.format(guid=os.getenv('LOCATION'), password=os.getenv('LOCATION_KEY'))
   else:
     location = "public: [\"AWS_US_EAST_1\"]"

   # SCRIPT_CONTENT = '''var assert = require('assert');

# $http.post('{url}',
  # {{
    # json: {{
    # query: '{{ schemaVersion }}'
    # }}
  # }},

  # function (err, response, body) {{
    # assert.equal(response.statusCode, 200, 'Expected a 200 OK response');
    # assert.ok('schemaVersion' in body.data);

    # console.log('Response:', body);
    # console.log('Response:', response.statusCode);
  # }}
# );'''.format(url=api['url'])

   monitor_found = False
   headers = {
       "Api-Key": key,
       "Content-Type": "application/json"
   }

   data = {"query":"{"
     "actor {"
       "entitySearch(query: \"domain = 'SYNTH' AND type = 'MONITOR'\") {"
         "results {"
           "entities {"
             "... on SyntheticMonitorEntityOutline {"
               "name\n"
               "guid"
             "}"
           "}"
         "}"
       "}"
     "}"
   "}", "variables":""}

   try:
     response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data), allow_redirects=False)
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
       monitor_id = x.get('guid')
       print('Monitor {} already exists, updating with the latest configuration.'.format(monitor_name))

       data = {"query":"mutation {"
         "syntheticsUpdateScriptApiMonitor ("
           "guid: \"" + monitor_id + "\","
           "monitor: {"
             "locations: {"
               "" + location + ""
             "},"
             "name: \"" + monitor_name + "\","
             "period: " + freq + ","
             "runtime: {"
               "runtimeType: \"NODE_API\","
               "runtimeTypeVersion: \"16.10\","
               "scriptLanguage: \"JAVASCRIPT\""
             "}"
             #"script: " + repr(SCRIPT_CONTENT) + ","
             "script: " + repr(api['query']) + ","
             "status: ENABLED,"
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
       "syntheticsCreateScriptApiMonitor ("
         "accountId: " + NR_ACCT_ID + ","
         "monitor: {"
           "locations: {"
             "" + location + ""
           "},"
           "name: \"" + monitor_name + "\","
           "period: " + freq + ","
           "runtime: {"
             "runtimeType: \"NODE_API\","
               "runtimeTypeVersion: \"16.10\","
               "scriptLanguage: \"JAVASCRIPT\""
           "}"
           #"script: " + repr(SCRIPT_CONTENT) + ","
           "script: " + repr(api['query']) + ","
           "status: ENABLED,"
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
     print("Monitor {} was created".format(monitor_name))