#!/usr/bin/env python

"usage: monitor.py request_type input [input_name=name]"

import os
import sys
import test_client


def base_url():
    environment = (os.getenv('DLENV') or '').lower()
    suffix = '' if environment == 'prod' else '-{}'.format(environment)
    return 'https://pdfprocess{}.datalogics-cloud.com'.format(suffix)

if __name__ == '__main__':
    response = test_client.run(sys.argv, base_url())
    if not response: sys.exit(response)
    response.save_output()
    print('created: {}'.format(response.output_filename))
