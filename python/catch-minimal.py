#!/usr/bin/env python
"""
Minimal Python script for moving target queries with the CATCH API.

CATCH is a search tool for finding comets and asteroids in NEO and time-domain
survey data, hosted by the Planetary Data System's Small Bodies Node:

https://catch.astro.umd.edu/

Requires: requests, sseclient

(requests and sseclient greatly simplifies listening to the CATCH event stream)

"""
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

# If 'queued' is True, listen to the CATCH event stream until our job ID is
# published.
if data['queued']:
    messages = SSEClient('https://catch.astro.umd.edu/catch/stream')
    for msg in messages:
        if msg.data == data['job_id']:
            break

# 'results' is the URL to the search results
res = requests.get(data['results'])

# response is JSON formatted
data = res.json()

print(data)
