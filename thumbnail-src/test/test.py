"thumbnail test client"

import os
import sys
import glob

test_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(test_dir))
requests_dir = glob.glob(os.path.join(root_dir, 'eggs', 'requests-*.egg'))[-1]
samples_dir = os.path.join(root_dir, 'samples', 'python')
sys.path[0:0] = [requests_dir, samples_dir]

import requests
from pdfclient import Response

BASE_URL = 'http://127.0.0.1:5050'

INPUT = {'inputURL': 'http://www.datalogics.com/pdf/doc/pdf2img.pdf'}
BAD_INPUT = {'inputURL': 'http://www.datalogics.com/pdf/doc/spam.pdf'}

def run(base_url=BASE_URL, data=None, params=None):
    data = data or {'options': '{"imageHeight": 160}'}
    return Response(requests.get(base_url, data=data, params=params))
