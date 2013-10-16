"server regression tests, input file(s)"

import os
import subprocess
from web_api.tmpdir import Stdout
from test_client import ProcessCode
from nose.tools import assert_equal, assert_in


def test_no_input():
    validate_error([], 'no input')

def test_one_file():
    validate_input(args(['data/hello_world.pdf']), ProcessCode.OK)

def test_two_files():
    validate_error(['data/hello_world.pdf', 'data/bad.pdf'], 'excess input')

def test_url_and_file():
    input = args(['data/bad.pdf']) + ['--form', 'inputURL=http://spam.pdf']
    validate_input(input, ProcessCode.InvalidInput, 'excess input')


def validate_error(input, error):
    validate_input(args(input), ProcessCode.InvalidInput, error)

def validate_input(input, process_code, error=None):
    with Stdout() as stdout:
        assert_equal(subprocess.call(input, stdout=stdout), process_code)
        if error: assert_in(error, str(stdout))

def args(input):
    result = ['scripts/curl']
    for file in input:
        result.extend(['--form', '%s=@%s' % (os.path.basename(file), file)])
    return result
