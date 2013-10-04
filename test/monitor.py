#!/usr/bin/env python

"server environment monitor"

import sys
import test_client


DEFAULT_ENVIRONMENT = 'prod'

def environment(argv):
    return argv[1] if 1 < len(argv) else DEFAULT_ENVIRONMENT

def base_url(argv):
    suffix = environment(argv)
    suffix = '' if suffix == DEFAULT_ENVIRONMENT else '-%s' % suffix
    return 'https://pdfprocess%s.datalogics-cloud.com' % suffix

if __name__ == '__main__':
    response = test_client.run(['data/four_pages.pdf'], base_url(sys.argv))
    if not response: sys.exit(response)
    response.save_image()
    print('created: %s' % response.image_filename)
