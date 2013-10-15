#!/usr/bin/env python

"usage: monitor.py"

import os
import sys

import test
import pdf2img


class MockPDF2IMG:
    input, output_form = os.path.basename(test.INPUT_URL), 'png'

def base_url():
    environment = (os.getenv('DLENV') or '').lower()
    environment_suffix = '' if environment == 'prod' else ('-%s' % environment)
    return 'http://thumbnail%s.datalogics-cloud.com' % environment_suffix

def pdf2img_response():
    image_response = test.run(base_url(), params=test.INPUT)
    return pdf2img.Response(MockPDF2IMG(), image_response)

if __name__ == '__main__':
    response = pdf2img_response()
    if not response: sys.exit(response)
    response.save_image()
    print('created: %s' % response.image_filename)
