#!/usr/bin/env python
"""
Minimal Python script for moving target queries with the CATCH API.

CATCH is a search tool for finding comets and asteroids in NEO and time-domain
survey data, hosted by the Planetary Data System's Small Bodies Node:

https://catch.astro.umd.edu/

Requires: requests, sseclient

(requests and sseclient greatly simplifies listening to the CATCH event stream)

"""
import json
import requests
from sseclient import SSEClient

# set up parameters, we are searching for comet 65P and do not want cached
# results
params = {
    'target': '65P',
    'cached': 'false'
}

# API route is .../query/moving
res = requests.get('https://catch.astro.umd.edu/catch/query/moving',
                   params=params)

# response is JSON formatted
data = res.json()

# If 'queued' is True, listen to the CATCH event stream until a message
# with our job ID prefix (first 8 characters) is 'success' or 'error'.
if data['queued']:
    messages = SSEClient('https://catch.astro.umd.edu/catch/stream')
    for message in messages:
        message_data = json.loads(message.data)

        # edit out keep-alive messages
        if not isinstance(message_data, dict):
            continue

        if message_data['job_prefix'] == data['job_id'][:8]:
            # this message is for us, print the text
            print(message_data['text'], file=sys.stderr)

        # Message status may be 'success', 'error', 'running', 'queued'.
        if message_data['status'] in ['error', 'success']:
            break

# 'results' is the URL to the search results
res = requests.get(data['results'])

# response is JSON formatted
data = res.json()

print(data)
