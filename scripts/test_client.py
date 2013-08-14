#!/usr/bin/env python

"pdf2img test client"

import glob
import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
requests_dir = glob.glob(os.path.join(root_dir, 'eggs', 'requests-*.egg'))[0]
sys.path[0:0] = [requests_dir, os.path.join(root_dir, 'samples', 'python')]

from pdf2img import PDF2IMG
from pdfclient import ProcessCode


API_KEY = 'f54ab5d8-5775-42c7-b888-f074ba892b57'
BASE_URL = 'https://pdfprocess-test.datalogics-cloud.com'
VERSION = 0

class StatusCode:
    OK = 200
    BadRequest = 400
    Forbidden = 403
    NotFound = 404
    RequestEntityTooLarge = 413
    UnsupportedMediaType = 415
    TooManyRequests = 429
    InternalServerError = 500

def pdf2img(api_key=API_KEY, version=VERSION, base_url=BASE_URL):
    return PDF2IMG(api_key, version, base_url)

def run(argv):
    return pdf2img()(argv)

if __name__ == '__main__':
    response = run(sys.argv)
    if not response: sys.exit(response)
    response.save_image()
    print('created: %s' % response.image_filename)

