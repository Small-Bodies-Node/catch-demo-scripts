#!/usr/bin/env python
"""
Minimal Python script for moving target queries with the CATCH API v2.0.

CATCH is a search tool for finding comets and asteroids in NEO and time-domain
survey data, hosted by the Planetary Data System's Small Bodies Node:

https://catch.astro.umd.edu/

Requires: requests, sseclient

OK, not a strictly minimal script, but requests and sseclient greatly simplify
listening to the CATCH event stream.

"""

import sys
import json
import requests
from sseclient import SSEClient

# Set up parameters:
#   * search for comet 65P
#   * do not retrieve cached results, but run a new search on the database
# See https://catch.astro.umd.edu/apis for other options.
params = {
    "target": "65P",
    "sources": "neat_palomar_tricam",
    "cached": "false"
}

base_url = "https://catch.astro.umd.edu/api"

# API route for searches is .../catch
res = requests.get(base_url + "/catch", params=params)

# response is JSON formatted
data = res.json()

# If 'queued' is True, listen to the CATCH event stream until a message
# with our job ID prefix (first 8 characters) is 'success' or 'error'.
if data['queued']:
    messages = SSEClient(base_url + "/stream")
    for message in messages:
        # ignore blank lines
        if message.data == "":
            continue

        message_data = json.loads(message.data)

        # edit out keep-alive messages
        if not isinstance(message_data, dict):
            continue

        if message_data["job_prefix"] == data["job_id"][:8]:
            # this message is for us, print the text
            print(message_data['text'], file=sys.stderr)
        else:
            continue

        # Message status may be "success", "error", "running", "queued".
        if message_data["status"] in ["error", "success"]:
            break

# "results" is the URL to the search results
res = requests.get(data["results"])

# response is JSON formatted
data = res.json()

print(json.dumps(data))
