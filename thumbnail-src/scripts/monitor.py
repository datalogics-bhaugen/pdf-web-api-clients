#!/usr/bin/env python

"usage: monitor.py output_filename"

import os
import sys
import subprocess


INPUT_URL = 'http://www.datalogics.com/pdf/doc/pdf2img.pdf'

def base_url():
    environment = (os.getenv('DLENV') or '').lower()
    suffix = '' if environment == 'prod' else '-{}'.format(environment)
    return 'http://thumbnail{}.datalogics-cloud.com'.format(suffix)

def monitor(argv):
    request_url = '{}?inputURL={}'.format(base_url(), INPUT_URL)
    subprocess.call(['curl', '--output', argv[1], request_url])

if __name__ == '__main__':
    monitor(sys.argv)
