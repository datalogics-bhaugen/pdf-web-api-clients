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
INPUT_NAME = 'inputName={}'.format(INPUT_FILE)

RENDER_PAGES_OPTIONS = {'outputFormat': 'jpg', 'printPreview': True}
OPTIONS = 'options={}'.format(json.dumps(RENDER_PAGES_OPTIONS))

FAKE_ID = '12345678'
FAKE_KEY = '1234567890abcdef1234567890abcdef'

client = test_client.client(FAKE_ID, FAKE_KEY)
client(['test', 'FlattenForm', INPUT_FILE, INPUT_NAME])
client(['test', 'RenderPages', test_client.INPUT_URL, OPTIONS])
