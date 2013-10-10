#!/usr/bin/env python

"pdf2img test client"

import glob
import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json_dir = glob.glob(os.path.join(root_dir, 'eggs', 'simplejson-*.egg'))[0]
requests_dir = glob.glob(os.path.join(root_dir, 'eggs', 'requests-*.egg'))[0]
samples_dir = os.path.join(root_dir, 'samples', 'python')
sys.path[0:0] = [json_dir, requests_dir, samples_dir]

from pdf2img import PDF2IMG
from pdfclient import Application, ImageProcessCode, ProcessCode


BASE_URL = 'https://pdfprocess-test.datalogics-cloud.com'

TEST_ID = '84445ec0'
TEST_KEY = '2d3eac77bb3b9bea69a91e625b9241d2'

class StatusCode:
    OK = 200
    BadRequest = 400
    Forbidden = 403
    NotFound = 404
    RequestEntityTooLarge = 413
    UnsupportedMediaType = 415
    TooManyRequests = 429
    InternalServerError = 500

def pdf2img(id=TEST_ID, key=TEST_KEY): return PDF2IMG(id, key)
def run(argv, base_url=BASE_URL): return pdf2img()(argv, base_url)

if __name__ == '__main__':
    response = run(sys.argv)
    if not response: sys.exit(response)
    response.save_image()
    print('created: %s' % response.image_filename)
