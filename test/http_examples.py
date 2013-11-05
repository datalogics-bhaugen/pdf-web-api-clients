#!/usr/bin/env python

'''
to capture HTTP request examples, run this script after reconfiguring
urllib3 logging by adding the following lines to samples/python/pdfclient.py:

import httplib
import logging
httplib.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
logger = logging.getLogger('requests.packages.urllib3')
logger.setLevel(logging.DEBUG)
logger.propagate = True

use scripts/replace_newline to make the output legible.
'''

import json
import test_client

INPUT_FILE = 'hello_world.pdf'  # copy or link data/hello_world.pdf
INPUT_NAME = 'input_name={}'.format(INPUT_FILE)
INPUT_URL = 'http://www.datalogics.com/pdf/doc/pdf2img.pdf'

RENDER_PAGES_OPTIONS = {'outputFormat': 'jpg', 'printPreview': True}
OPTIONS = 'options={}'.format(json.dumps(RENDER_PAGES_OPTIONS))

BASE_URL = 'http://pdfprocess.datalogics-cloud.com'
FAKE_ID = '12345678'
FAKE_KEY = '1234567890abcdef1234567890abcdef'

client = test_client.client(FAKE_ID, FAKE_KEY)
client(['test', 'FlattenForm', INPUT_FILE, INPUT_NAME], BASE_URL)
client(['test', 'RenderPages', INPUT_URL, OPTIONS], BASE_URL)
