#!/usr/bin/env python

"usage: monitor.py <input filename>"

import os
import sys
import test_client


def base_url():
    environment = (os.getenv('DLENV') or '').lower()
    environment_suffix = '' if environment == 'prod' else ('-%s' % environment)
    return 'https://pdfprocess%s.datalogics-cloud.com' % environment_suffix

if __name__ == '__main__':
    response = test_client.run([sys.argv[1]], base_url())
    if not response: sys.exit(response)
    response.save_image()
    print('created: %s' % response.image_filename)
