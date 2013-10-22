#!/usr/bin/env python

"usage: monitor.py request_type input_filename output_filename"

import os
import sys
import json
import subprocess

import cfg
from itertools import chain


THREE_SCALE = cfg.Configuration.three_scale


def base_url():
    dlenv = cfg.Configuration.environment.dlenv
    suffix = '' if dlenv == 'prod' else '-{}'.format(dlenv)
    return 'https://pdfprocess{}.datalogics-cloud.com'.format(suffix)

def monitor(argv):
    id, key = THREE_SCALE.test_id, THREE_SCALE.test_key
    application_json = json.dumps({'id': id, 'key': key})
    application = 'application={}'.format(application_json).replace(' ', '')
    parts = (application, 'input=@{}'.format(argv[2]), 'inputName=monitor')
    form_parts = list(chain.from_iterable(('--form', part) for part in parts))
    url = '{}/api/actions/{}'.format(base_url(), argv[1])
    args = ['curl', '--insecure'] + form_parts + ['--output', argv[3], url]
    subprocess.call(args)

if __name__ == '__main__':
    monitor(sys.argv)
