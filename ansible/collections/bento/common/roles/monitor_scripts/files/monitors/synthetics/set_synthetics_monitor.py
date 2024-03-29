#!/usr/bin/python

import os
import json
import requests
import re
import time
from tags import set_tags_nrql
from monitors.alerts.conditions.synthetics import set_synthetics_condition

def setsyntheticsmonitor(project, tier, key, api, policy_id):
   API_ENDPOINT = 'https://synthetics.newrelic.com/synthetics/api/v3/monitors'

   if tier.lower() == 'prod':
     freq = 10
   else:
     freq = 30

   # set monitor configuration
   monitor_name = '{} {} {} Monitor'.format(project, tier, api['name'])
   data = {
       "name": monitor_name,
       "type": "BROWSER",
       "frequency": freq,
       "uri": api['url'],
       "locations": [ api['location'] ],
       "status": "ENABLED",
       "slaThreshold": 7.0,
   }
   
   monitor_found = False
   headers = {'Api-Key': key}
   
   try:
     response = requests.get('{}'.format(API_ENDPOINT), headers=headers)
   except requests.exceptions.RequestException as e:
     raise SystemExit(e)

   for x in response.json()['monitors']:
     if monitor_name in x.get("name", "none").lower():
       monitor_found = True

   if not monitor_found:
     headers = {
         "Api-Key": key,
         "Content-Type": "application/json"
     }

     try:
       response = requests.post('{}'.format(API_ENDPOINT), headers=headers, data=json.dumps(data), allow_redirects=False)
     except requests.exceptions.RequestException as e:
       raise SystemExit(e)
     
     location = response.headers.get('location')

   else:
     print('{} already exists - updating with current configuration'.format(monitor_name))

     headers = {
         "Api-Key": key,
         "Content-Type": "application/json"
     }

     try:
       requests.put('{}/{}'.format(API_ENDPOINT, x.get("id", "none")), headers=headers, data=json.dumps(data), allow_redirects=False)
     except requests.exceptions.RequestException as e:
       raise SystemExit(e)

   # get the newly created monitor
   # pause to allow it to be created
   time.sleep(15)
   try:
     response = requests.get('{}'.format(API_ENDPOINT), headers=headers)
   except requests.exceptions.RequestException as e:
     raise SystemExit(e)

   for x in response.json()['monitors']:
     if monitor_name in x.get("name", "none"):
       current_monitor = x

   # set tags on the monitor
   set_tags_nrql.settagsnrql(project, tier, current_monitor.get('name'), key)

   # add synthetics condition
   set_synthetics_condition.setcondition(project, tier, key, api['name'].lower(), current_monitor.get('id'), policy_id)