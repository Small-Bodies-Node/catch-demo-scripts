#!/usr/bin/env python
import sys
import argparse
import requests
from uuid import UUID
from sseclient import SSEClient
from astropy.table import Table


def query_moving(args):
    """Catch a moving object with query/moving route.

    A CATCH moving target query is a multi-part process:
      1. Request the search.
         A. If the search was cached, continue.
         B. If a new search needs to be executed, monitor the job event
            stream and wait for the search to complete.
      2. Retrieve the results.

    """

    # Set up parameters
    params = {
        'target': args.target,
        'cached': str(args.cached).lower()
    }

    # API route is .../query/moving
    res = requests.get('{}/query/moving'.format(args.base), params=params)

    # response is JSON formatted
    data = res.json()

    # If 'queued' is True...
    if data['queued']:
        # listen to event stream
        messages = SSEClient('{}/stream'.format(args.base))
        print('Waiting for job ID {} to complete...'.format(
            data['job_id']), file=sys.stderr)

        # Cycle through the messages.  When our job ID is published to the
        # stream, results are ready.
        for msg in messages:
            if msg.data == data['job_id']:
                break
        print('...completed.', file=sys.stderr)

    # 'results' is the URL to the search results
    res = requests.get(data['results'])

    # response is JSON formatted
    data = res.json()

    # print the data
    if 'data' in data:
        format_caught_data(data, args.format)
    else:
        # No data?  There should be an error message, but if not, print "unknown error"
        msg = data.get('message', 'unknown error')
        print('{}'.format(msg, file=sys.stderr))


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
        format_caught_data(data, args.format)
    else:
        # No data?  There should be an error message, but if not, print "unknown error"
        msg = data.get('message', 'unknown error')
        print('{}'.format(msg, file=sys.stderr))


def caught_labels(args):
    """Retrieve descriptions for caught fields/columns."""

    # API route is .../caught/labels (no parameters)
    res = requests.get('{}/caught/labels'.format(args.base))

    # response is JSON formatted
    data = res.json()
    print(data)


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


def format_caught_data(data, format):
    """Format caught data: 'table' or 'json'."""

    # 'count' indicates how many times the object was found
    if data['count'] > 0:
        if format == 'table':
            tab = Table(data['data'])
            tab.pprint(-1, -1)
        else:
            # user requested json format
            print(data)
    else:
        print('Nothing found.', file=sys.stderr)


# command-line interface
parser = argparse.ArgumentParser()
parser.add_argument('--base', default='https://catch.astro.umd.edu/catch',
                    help='base URL for query, e.g., https://host/location')

subparsers = parser.add_subparsers(title='API routes')

# API route .../caught/{job_id}
parser_caught = subparsers.add_parser(
    'caught', help='retrieve caught object data')
parser_caught.add_argument('jobid', help='user job ID')
parser_caught.add_argument('--format', choices=['json', 'table'],
                           default='table', help='output format')
parser_caught.set_defaults(func=caught)

# API route .../caught/labels
parser_caught = subparsers.add_parser(
    'caught/labels', help='retrieve descriptions for caught field/columns')
parser_caught.set_defaults(func=caught_labels)

# API route .../query/moving
parser_moving = subparsers.add_parser(
    'query/moving', help='search for a target')
parser_moving.add_argument('target', help='moving target designation')
parser_moving.add_argument('--force', dest='cached', action='store_false',
                           help=('do not use cached results and force a '
                                 'new query'))
parser_moving.add_argument('--format', choices=['json', 'table'],
                           default='table', help='output format')
parser_moving.set_defaults(func=query_moving)

# API route .../stream
parser_stream = subparsers.add_parser(
    'stream', help='inspect CATCH event stream')
parser_stream.set_defaults(func=listen_to_stream)

args = parser.parse_args()
if hasattr(args, 'func'):
    args.func(args)
else:
    parser.print_help()
