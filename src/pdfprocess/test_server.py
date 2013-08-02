'pdfclient regression tests'

import exceptions
import os
import sys
from nose.tools import assert_equal, assert_in, raises

src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir = os.path.dirname(src_dir)
sys.path[0:0] = [os.path.join(root_dir, 'samples', 'python')]
import pdfclient


BASE_URL = 'http://127.0.0.1:5000'


def test_bad_version():
    pdf_client = pdfclient.Client('api-key', -1, BASE_URL)
    image_request = pdf_client.make_request('image')
    with open(__file__, 'rb') as input:
        response = image_request.post(input, 'TIF')
    assert_equal(response.status_code, 404)

