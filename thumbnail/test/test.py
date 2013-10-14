"thumbnail test client"

import os
import sys
import glob

test_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(test_dir))
json_dir = glob.glob(os.path.join(root_dir, 'eggs', 'simplejson-*.egg'))[0]
requests_dir = glob.glob(os.path.join(root_dir, 'eggs', 'requests-*.egg'))[0]
samples_dir = os.path.join(root_dir, 'samples', 'python')
sys.path[0:0] = [json_dir, requests_dir, samples_dir]

import requests
from pdfclient import ImageResponse


BASE_URL = 'http://127.0.0.1:5050'
INPUT_URL = 'http://www.datalogics.com/pdf/doc/pdf2img.pdf'
INPUT = {'inputURL': INPUT_URL}

def run(base_url=BASE_URL, data=None, params=None):
    options = {'options': '{"imageHeight": 150}'}
    if data: options.update(data)
    return ImageResponse(requests.get(base_url, data=options, params=params))
