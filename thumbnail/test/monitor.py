#!/usr/bin/env python

"usage: monitor.py [inputName]"

import os
import sys

import test
import pdfprocess


def base_url():
    environment = (os.getenv('DLENV') or '').lower()
    suffix = '' if environment == 'prod' else '-{}'.format(environment)
    return 'http://thumbnail{}.datalogics-cloud.com'.format(suffix)

def pdfprocess_response(argv):
    input_name = os.path.basename(test.INPUT_URL) if len(argv) < 2 else argv[1]
    data = {'inputName': input_name}
    client_response = test.run(base_url(), data=data, params=test.INPUT)
    output_filename = '{}.png'.format(os.path.splitext(input_name)[0])
    return pdfprocess.Response(client_response, output_filename)

if __name__ == '__main__':
    response = pdfprocess_response(sys.argv)
    if not response: sys.exit(response)
    response.save_output()
    print('created: {}'.format(response.output_filename))
