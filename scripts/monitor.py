#!/usr/bin/env python

"usage: monitor.py request_type input_filename output_filename"

import os
import sys
import subprocess
from itertools import chain


APP = 'application={"id":"84445ec0","key":"2d3eac77bb3b9bea69a91e625b9241d2"}'


def base_url():
    environment = (os.getenv('DLENV') or '').lower()
    suffix = '' if environment == 'prod' else '-{}'.format(environment)
    return 'https://pdfprocess{}.datalogics-cloud.com'.format(suffix)

def monitor(argv):
    url = '{}/api/actions/{}'.format(base_url(), argv[1])
    parts = (APP, 'input=@{}'.format(argv[2]), 'inputName=monitor')
    form_parts = list(chain.from_iterable(('--form', part) for part in parts))
    subprocess.call(['curl'] + form_parts + ['--output', argv[3], url])

if __name__ == '__main__':
    monitor(sys.argv)
