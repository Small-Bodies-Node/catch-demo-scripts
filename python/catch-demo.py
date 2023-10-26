#!/usr/bin/env python
"""
Fully functional Python script for CATCH API v2.0.

CATCH is a search tool for finding comets and asteroids in NEO and time-domain
survey data, hosted by the Planetary Data System's Small Bodies Node:

https://catch.astro.umd.edu/

Requires: astropy, requests, and sseclient

"""
import sys
import argparse
import requests
import json
from uuid import UUID
from sseclient import SSEClient
try:
    from astropy.table import Table
    default_format = 'table'
except ImportError:
    Table = None
    default_format = 'json'


def sources(args):
    """Inspect API for allowed sources."""

    # API route is .../catch
    res = requests.get('{}/openapi.json'.format(args.base))

    # response is JSON formatted
    spec = res.json()

    parameters: list = spec['paths']['/catch']['get']['parameters']
    sources = [
        parameter["schema"]["items"]["enum"]
        for parameter in parameters
        if parameter["name"] == "sources"
    ][0]

    print("Allowed sources:\n  ", end='')
    print("\n  ".join(sources))


def catch(args):
    """Catch a moving object with catch route.

    A CATCH moving target query is a multi-part process:
      1. Request the search.
         A. If the search was cached, continue.
         B. If a new search needs to be executed, monitor the job event
            stream and wait for the search to complete.
      2. Retrieve the results.

    """

    # Set up query parameters
    params = {
        "target": args.target,
        "cached": args.cached,
    }
    if args.uncertainty_ellipse:
        params["uncertainty_ellipse"] = args.uncertainty_ellipse

    if args.sources != []:
        params["sources"] = args.sources

    if args.padding is not None:
        params["padding"] = args.padding

    # API route is .../catch
    res = requests.get('{}/catch'.format(args.base), params=params)

    # response is JSON formatted
    data = res.json()

    # if 'results' is missing, an error occured
    if data.get('results') is None:
        # There should be an error message, but if not, print "unknown error"
        msg = data.get('message', 'unknown error')
        print('{}'.format(msg), file=sys.stderr)
        return

    print("Job ID:", data["job_id"], file=sys.stderr)
    if "queue_full" in data:
        print("Queue full:", data["queue_full"], file=sys.stderr)
    print("Queued:", data["queued"], file=sys.stderr)
    print("Message:", data["message"], file=sys.stderr)
    print("Results URL:", data["results"], file=sys.stderr)

    # If 'queued' is True, listen to the CATCH event stream until a message
    # with our job ID prefix (first 8 characters) is 'success' or 'error'.
    if data['queued']:
        # listen to event stream
        messages = SSEClient('{}/stream'.format(args.base))
        print('Connected to stream...', file=sys.stderr)

        # cycle through the messages
        for message in messages:
            # ignore blank lines
            if message.data == "":
                continue

            message_data = json.loads(message.data)

            # edit out keep-alive messages
            if not isinstance(message_data, dict):
                continue

            # is this message for us?
            if message_data['job_prefix'] == data['job_id'][:8]:
                # print the message text
                print(message_data['text'], file=sys.stderr)

                # message status may be 'success', 'error', 'running', 'queued'
                if message_data['status'] in ['error', 'success']:
                    break

    # 'results' is the URL to the search results
    res = requests.get(data['results'])

    # response is JSON formatted
    data = res.json()

    # print the data
    if 'data' in data:
        # 'count' indicates how many times the object was found
        if data['count'] > 0:
            format_data(data["data"], args.format)
        else:
            print('Nothing found.', file=sys.stderr)
    else:
        # No data?  There should be an error message, but if not, print "unknown error"
        msg = data.get('message', 'unknown error')
        print(str(msg), file=sys.stderr)


def caught(args):
    """Retrieve and display caught data."""

    # validate job ID is UUID version 4, convert to hexadecimal string
    job_id = UUID(args.jobid, version=4).hex

    # API route is .../caught/{job_id} (no parameters)
    res = requests.get('{}/caught/{}'.format(args.base, job_id))

    # response is JSON formatted
    data = res.json()

    # print the data
    if 'data' in data:
        # 'count' indicates how many times the object was found
        if data['count'] > 0:
            format_data(data["data"], args.format)
        else:
            print('Nothing found.', file=sys.stderr)
    else:
        # No data?  There should be an error message, but if not, print "unknown error"
        msg = data.get('message', 'unknown error')
        print('{}'.format(msg, file=sys.stderr))


def status_sources(args):
    """Retrieve and display source database summary."""

    # API route is .../status/sources
    res = requests.get('{}/status/sources'.format(args.base))

    # response is JSON formatted
    data = res.json()

    if res.ok:
        format_data(data, args.format)
    else:
        print(str(data), file=sys.stderr)


def status_job_id(args):
    """Retrieve and display job status."""

    # validate job ID is UUID version 4, convert to hexadecimal string
    job_id = UUID(args.jobid, version=4).hex

    # API route is .../status/{job_id}
    res = requests.get('{}/status/{}'.format(args.base, job_id))

    # response is JSON formatted
    data = res.json()
    if res.ok:
        # print the data
        if 'status' in data:
            print(f"""# job_id: {data["job_id"]}
# target: {data["parameters"]["target"]}
# padding: {data["parameters"]["padding"]}
# uncertainty_ellipse: {data["parameters"]["uncertainty_ellipse"]}
""")
            format_data(data["status"], args.format)
    else:
        print(str(data), file=sys.stderr)


def listen_to_stream(args):
    """Inspect the CATCH event stream."""

    # API route is .../stream
    messages = SSEClient('{}/stream'.format(args.base))
    print('Listening to CATCH notification stream.  Use ctrl-c to stop.',
          file=sys.stderr)

    try:
        for msg in messages:
            print(msg)
    except KeyboardInterrupt:
        pass


def format_data(data, format):
    """Format dictionary as a string or a table."""
    if format == 'table':
        if Table is None:
            raise ImportError("table format requires astropy")
        tab = Table(data)
        tab.pprint(-1, -1)
    else:
        print(json.dumps(data, indent=2))


# command-line interface
parser = argparse.ArgumentParser()
parser.add_argument('--base', default='https://catch-api.astro.umd.edu',
                    help='base URL for query, e.g., https://catch-api.astro.umd.edu')

subparsers = parser.add_subparsers(title='API routes')

# show allowed sources
parser_sources = subparsers.add_parser("sources", help="show allowed sources")
parser_sources.set_defaults(func=sources)

# API route .../catch
parser_catch = subparsers.add_parser(
    'catch', help='search for a moving target')
parser_catch.add_argument('target', help='moving target designation')
parser_catch.add_argument("--padding", type=float,
                          help="pad ephemeris (arcmin)")
parser_catch.add_argument("--uncertainty-ellipse", action="store_true",
                          help="search using ephemeris uncertainty")
parser_catch.add_argument("--source", dest="sources", type=str,
                          action="append", help="search this data source")
parser_catch.add_argument('--force', dest='cached', action='store_false',
                          help=('do not use cached results and force a '
                                'new query'))
parser_catch.add_argument('--format', choices=['json', 'table'],
                          default=default_format,
                          help='output format')
parser_catch.set_defaults(func=catch)

# API route .../caught/{job_id}
parser_caught = subparsers.add_parser(
    'caught', help='retrieve caught object data')
parser_caught.add_argument('jobid', help='user job ID')
parser_caught.add_argument('--format', choices=['json', 'table'],
                           default='table', help='output format')
parser_caught.set_defaults(func=caught)

# API route .../status/{job_id}
parser_caught = subparsers.add_parser(
    'status/job_id', help='retrieve job status')
parser_caught.add_argument('jobid', help='user job ID')
parser_caught.add_argument('--format', choices=['json', 'table'],
                           default='table', help='output format')
parser_caught.set_defaults(func=status_job_id)

# API route .../status/sources
parser_caught = subparsers.add_parser(
    'status/sources', help='retrieve source database summary')
parser_caught.add_argument('--format', choices=['json', 'table'],
                           default='table', help='output format')
parser_caught.set_defaults(func=status_sources)

# API route .../stream
parser_stream = subparsers.add_parser(
    'stream', help='inspect CATCH event stream')
parser_stream.set_defaults(func=listen_to_stream)

args = parser.parse_args()
if hasattr(args, 'func'):
    args.func(args)
else:
    parser.print_help()
