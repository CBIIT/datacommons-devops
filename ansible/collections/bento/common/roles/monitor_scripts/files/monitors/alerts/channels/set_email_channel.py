#!/usr/bin/python

import os
import json
import requests

def setalertemailchannel(channel_name, destination_id, key):
   API_ENDPOINT = 'https://api.newrelic.com/graphql'
   NR_ACCT_ID = os.getenv('NR_ACCT_ID')

   channel_found = False
   headers = {
       "Api-Key": key,
       "Content-Type": "application/json"
   }

   data = {"query":"{"
     "actor {"
       "account(id: " + NR_ACCT_ID + ") {"
         "aiNotifications {"
           "channels {"
             "entities {"
               "id\n"
               "name\n"
               "product"
             "}"
             "error {"
               "details"
             "}"
           "}"
         "}"
       "}"
     "}"
   "}", "variables":""}

   try:
     response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data), allow_redirects=False)
   except requests.exceptions.RequestException as e:
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
     if channel_name in x.get("name", "none"):
       channel_found = True
       channel_id = x.get('id')

       data = {"query":"mutation {"
           "aiNotificationsUpdateDestination(accountId: " + NR_ACCT_ID + ", destinationId: \"" + destination_id + "\", destination: {"
             "name: \"" + channel_name + "\""
           "}) {"
             "destination {"
               "id\n"
               "name"
             "}"
           "}"
       "}", "variables":""}

       try:
         response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data), allow_redirects=False)
       except requests.exceptions.RequestException as e:
         raise SystemExit(e)

   if not channel_found:
     data = {"query":"mutation {"
         "aiNotificationsCreateChannel(accountId: " + NR_ACCT_ID + ", channel: {"
           "type: EMAIL,"
           "name: \"" + channel_name + "\","
           "destinationId: \"" + destination_id + "\","
           "product: IINT,"
           "properties: []"
         "}) {"
           "channel {"
             "id\n"
             "name"
           "}"
         "}"
     "}", "variables":""}

     try:
       response = requests.post('{}'.format(API_ENDPOINT), headers=headers, data=json.dumps(data), allow_redirects=False)
     except requests.exceptions.RequestException as e:
       raise SystemExit(e)
     print("Channel {} was created".format(channel_name))
     channel_id = response.json()['data']['aiNotificationsCreateChannel']['channel']['id']
   else:
     print("Channel {} was found".format(channel_name))

   return(channel_id)