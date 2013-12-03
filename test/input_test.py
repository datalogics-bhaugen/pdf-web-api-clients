"server regression tests, input file(s)"

import os
import json
import subprocess
from server.tmpdir import Stdout
from test_client import ErrorCode
from nose.tools import assert_equal


def test_no_input():
    validate_error([], 'request missing "input" or "inputURL" part')

def test_one_file():
    validate_input(args(['data/hello_world.pdf']))

def test_two_files():
    return  # TODO: need another way to test this
    error = 'excess input (2 files)'
    validate_error(['data/hello_world.pdf', 'data/bad.pdf'], error)

def test_url_and_file():
    error = 'excess input (inputURL and request file)'
    input = args(['data/bad.pdf']) + ['--form', 'inputURL=http://spam.pdf']
    validate_input(input, ErrorCode.InvalidInput, error)


def validate_error(input, error):
    validate_input(args(input), ErrorCode.InvalidInput, error)

def validate_input(input, error_code=0, error_message=None):
    with Stdout() as stdout:
        subprocess.call(input, stdout=stdout)
        if error_code:
            response = json.loads(str(stdout))
            assert_equal(error_code, response['errorCode'])
            assert_equal(error_message, response['errorMessage'])

def args(input):
    result = ['scripts/curl']
    for file in input:
        result.extend(['--form', 'input=@{}'.format(file)])
    return result
