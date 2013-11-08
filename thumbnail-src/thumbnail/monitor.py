#!/usr/bin/env python

'''
usage: monitor.py output_filename [service_url]
monitor.py pdf2img.png http://127.0.0.1:5050
'''


import os
import sys
import subprocess

import cfg


INPUT_URL = 'http://www.datalogics.com/pdf/doc/pdf2img.pdf'

def base_url(argv):
    if len(argv) > 2: return argv[2]
    dlenv = cfg.Configuration.environment.dlenv
    suffix = '' if dlenv == 'prod' else '-{}'.format(dlenv)
    return 'http://thumbnail{}.datalogics-cloud.com'.format(suffix)

def monitor(argv):
    if len(argv) < 2: sys.exit(__doc__)
    query_string = 'imageHeight=160&inputURL={}'.format(INPUT_URL)
    request_url = '{}/?{}'.format(base_url(argv), query_string)
    subprocess.call(['curl', '--output', argv[1], request_url])

if __name__ == '__main__':
    monitor(sys.argv)
