#!/usr/bin/env python
"""
Minimal Python script for fixed target queries with the CATCH API v3.0.

CATCH is a search tool for searching time-domain survey data, hosted by the
Planetary Data System's Small Bodies Node:

https://catch.astro.umd.edu/

Requires: requests

"""

import json
import requests

# Set up parameters:
#   * search for observations covering the center of M15
# See https://catch-api.astro.umd.edu/ui for RA, Dec formats and other options.
params = {"ra": "21:29:58", "dec": "+12:10:01", "sources": "neat_palomar_tricam"}

base_url = "https://catch-api.astro.umd.edu"

# API route for searches is .../fixed
res = requests.get(base_url + "/fixed", params=params)

# response is JSON formatted
data = res.json()

# response is JSON formatted
data = res.json()

print(json.dumps(data))
