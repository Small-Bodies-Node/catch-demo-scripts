"""Tests output from catch-minimal.py and catch-demo.py"""

import json
from subprocess import check_output
from astropy.io import ascii
import pytest


def test_catch_demo():
    output = check_output(
        ['python', 'catch-demo.py', 'query/moving', '65P', '--force', '--format=table'])
    data = ascii.read(output.decode())

    assert len(data) == 15


def test_catch_minimal():
    output = check_output(['python', 'catch-minimal.py'])
    data = json.loads(output.decode())

    assert len(data['data']) == 15
