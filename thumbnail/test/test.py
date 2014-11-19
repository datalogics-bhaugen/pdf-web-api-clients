"thumbnail test client"

import os
import sys
import glob

test_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(test_dir))
requests_dir = glob.glob(os.path.join(root_dir, 'eggs', 'requests-*.egg'))[-1]
samples_dir = os.path.join(root_dir, 'samples', 'python')
sys.path[0:0] = [root_dir, requests_dir, samples_dir]

import requests

from server import cfg
from pdfclient import Response

THUMBNAIL_PORT = cfg.Configuration.service.thumbnail_port
BASE_URL = 'http://127.0.0.1:{}'.format(THUMBNAIL_PORT)

INPUT_URL = cfg.Configuration.test.input_url
BAD_URL = os.path.join(os.path.dirname(INPUT_URL), 'spam.pdf')

INPUT = {'inputURL': INPUT_URL}
BAD_INPUT = {'inputURL': BAD_URL}

def run(base_url=BASE_URL, data=None, params=None):
    data = data or {'options': '{"imageHeight": 160}'}
    return Response(requests.get(base_url, data=data, params=params))
