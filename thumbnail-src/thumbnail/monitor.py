#!/usr/bin/env python

'''
usage: monitor.py output_filename
example: monitor.py pdf2img.png
'''


import os
import sys
import subprocess

import cfg


INPUT_URL = 'http://www.datalogics.com/pdf/doc/pdf2img.pdf'

def base_url():
    dlenv = cfg.Configuration.environment.dlenv
    suffix = '' if dlenv == 'prod' else '-{}'.format(dlenv)
    return 'http://thumbnail{}.datalogics-cloud.com'.format(suffix)

def monitor(argv):
    query_string = 'imageHeight=160&inputURL={}'.format(INPUT_URL)
    request_url = '{}/?{}'.format(base_url(), query_string)
    subprocess.call(['curl', '--output', argv[1], request_url])

if __name__ == '__main__':
    monitor(sys.argv)
