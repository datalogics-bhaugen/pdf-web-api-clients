#!/usr/bin/env python

"pdfprocess test client"

import glob
import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json_dir = glob.glob(os.path.join(root_dir, 'eggs', 'simplejson-*.egg'))[0]
requests_dir = glob.glob(os.path.join(root_dir, 'eggs', 'requests-*.egg'))[0]
samples_dir = os.path.join(root_dir, 'samples', 'python')
sys.path[0:0] = [json_dir, requests_dir, samples_dir]

import requests
from pdfclient import Application, ErrorCode, RenderPages
from pdfprocess import Client


BASE_URL = 'https://pdfprocess-test.datalogics-cloud.com'

TEST_ID = '84445ec0'
TEST_KEY = '2d3eac77bb3b9bea69a91e625b9241d2'

class HTTPCode:
    OK = requests.codes.ok
    BadRequest = requests.codes.bad_request
    Forbidden = requests.codes.forbidden
    NotFound = requests.codes.not_found
    RequestEntityTooLarge = requests.codes.request_entity_too_large
    UnsupportedMediaType = requests.codes.unsupported_media_type
    TooManyRequests = requests.codes.too_many_requests
    InternalServerError = requests.codes.internal_server_error

def client(id=TEST_ID, key=TEST_KEY): return Client(id, key)
def run(argv, base_url=BASE_URL): return client()(argv, base_url)

if __name__ == '__main__':
    response = run(sys.argv)
    if not response: sys.exit(response)
    response.save_output()
    print('created: {}'.format(response.output_filename))
