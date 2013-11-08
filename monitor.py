#!/usr/bin/env python

'''
usage: monitor.py request_type input_filename output_filename [service_url]
monitor.py flatten/form test/data/annotated_form.pdf test.pdf
monitor.py render/pages test/data/four_pages.pdf test.png http://127.0.0.1:5000
'''


import os
import sys
import json
import subprocess

import cfg
from itertools import chain


THREE_SCALE = cfg.Configuration.three_scale


def base_url(argv):
    if len(argv) > 4: return argv[4]
    dlenv = cfg.Configuration.environment.dlenv
    suffix = '' if dlenv == 'prod' else '-{}'.format(dlenv)
    return 'https://pdfprocess{}.datalogics-cloud.com'.format(suffix)

def monitor(argv):
    if len(argv) < 4: sys.exit(__doc__)
    id, key = THREE_SCALE.test_id, THREE_SCALE.test_key
    application_json = json.dumps({'id': id, 'key': key})
    application = 'application={}'.format(application_json).replace(' ', '')
    parts = (application, 'input=@{}'.format(argv[2]), 'inputName=monitor')
    form_parts = list(chain.from_iterable(('--form', part) for part in parts))
    url = '{}/api/actions/{}'.format(base_url(argv), argv[1])
    args = ['curl', '--insecure'] + form_parts + ['--output', argv[3], url]
    subprocess.call(args)

if __name__ == '__main__':
    monitor(sys.argv)
