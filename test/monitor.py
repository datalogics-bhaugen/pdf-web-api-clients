#!/usr/bin/env python

"usage: monitor.py <input filename> [prod|test]"

import sys
import test_client


DEFAULT_ENVIRONMENT = 'prod'

def input(argv):
    return argv[1]

def environment(argv):
    return argv[2] if 2 < len(argv) else DEFAULT_ENVIRONMENT

def base_url(argv):
    suffix = environment(argv)
    suffix = '' if suffix == DEFAULT_ENVIRONMENT else '-%s' % suffix
    return 'https://pdfprocess%s.datalogics-cloud.com' % suffix

if __name__ == '__main__':
    response = test_client.run([input(sys.argv)], base_url(sys.argv))
    if not response: sys.exit(response)
    response.save_image()
    print('created: %s' % response.image_filename)
