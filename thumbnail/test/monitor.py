#!/usr/bin/env python

"usage: monitor.py"

import os
import sys

import test
import pdfprocess


def base_url():
    environment = (os.getenv('DLENV') or '').lower()
    suffix = '' if environment == 'prod' else '-{}'.format(environment)
    return 'http://thumbnail{}.datalogics-cloud.com'.format(suffix)

def pdfprocess_response():
    input_name = os.path.basename(test.INPUT_URL)
    output_filename = '{}.png'.format(os.path.splitext(input_name)[0])
    client_response = test.run(base_url(), params=test.INPUT)
    return pdfprocess.Response(client_response, output_filename)

if __name__ == '__main__':
    response = pdfprocess_response()
    if not response: sys.exit(response)
    response.save_output()
    print('created: {}'.format(response.output_filename))
