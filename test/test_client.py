#!/usr/bin/env python

"pdfprocess test client"

import glob
import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
requests_dir = glob.glob(os.path.join(root_dir, 'eggs', 'requests-*.egg'))[-1]
samples_dir = os.path.join(root_dir, 'samples', 'python')
sys.path[0:0] = [root_dir, requests_dir, samples_dir]

import cfg
import requests
from pdfclient import ErrorCode, RenderPages
from pdfprocess import Client


BASE_URL = 'https://pdfprocess-test.datalogics-cloud.com'
INPUT_URL = cfg.Configuration.test.input_url
THREE_SCALE = cfg.Configuration.three_scale

class HTTPCode:
    OK = requests.codes.ok
    BadRequest = requests.codes.bad_request
    Forbidden = requests.codes.forbidden
    NotFound = requests.codes.not_found
    RequestEntityTooLarge = requests.codes.request_entity_too_large
    UnsupportedMediaType = requests.codes.unsupported_media_type
    TooManyRequests = requests.codes.too_many_requests
    InternalServerError = requests.codes.internal_server_error

def client(id=THREE_SCALE.test_id, key=THREE_SCALE.test_key):
    return Client(id, key)

def run(argv, base_url=BASE_URL):
    return client()(argv, base_url)

if __name__ == '__main__':
    response = run(sys.argv)
    if not response.ok: sys.exit(response)
    response.save_output()
    print('created: {}'.format(response.output_filename))
