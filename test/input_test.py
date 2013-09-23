"server regression tests, input file(s)"

import os
import subprocess
from pdfprocess.stdout import Stdout
from test_client import ProcessCode
from nose.tools import assert_equal, assert_in


def test_hello_world():
    validate_input(['data/hello_world.pdf'], ProcessCode.OK)

def test_excess_input():
    validate_error(['data/hello_world.pdf', 'data/bad.pdf'], 'excess input')

def test_no_input():
    validate_error([], 'no input')


def validate_error(input, error):
    validate_input(input, ProcessCode.InvalidInput, error)

def validate_input(input, process_code, error=None):
    with Stdout() as stdout:
        assert_equal(subprocess.call(args(input), stdout=stdout), process_code)
        if error: assert_in(error, str(stdout))

def args(input):
    result = ['scripts/curl']
    for file in input:
        result.extend(['--form', '%s=@%s' % (os.path.basename(file), file)])
    return result

