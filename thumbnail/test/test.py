"thumbnail regression tests"

import subprocess
from nose.tools import assert_equal

import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[0:0] = [os.path.join(parent_dir, 'thumbnail')]
from tmpdir import Stdout


BASE_URL = '127.0.0.1:5050'
INPUT_URL = 'inputURL=%s' % 'http://www.datalogics.com/pdf/doc/pdf2img.pdf'

def test_form_data_url(): curl_request(['--form', INPUT_URL, BASE_URL])
def test_query_string_url(): curl_request(['%s?%s' % (BASE_URL, INPUT_URL)])

# TODO: add test that creates image file

def curl_request(request_input):
    input = ['curl', '--request', 'GET'] + request_input
    assert_equal(subprocess.call(input, stdout=Stdout(), stderr=Stdout()), 0)
