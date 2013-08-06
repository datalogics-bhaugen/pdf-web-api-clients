#!/usr/bin/env python

import os
import sys

import pdfclient


## pdf2img emulator
class PDF2IMG(object):
    BASE_URL = pdfclient.Client.BASE_URL
    VERSION = pdfclient.Client.VERSION
    ## @param api_key from [3scale](http://datalogics-cloud.3scale.net/)
    def __init__(self, api_key, version=VERSION, base_url=BASE_URL):
        self._api_key = api_key
        self._base_url = base_url
        self._version = version

    ## @param argv e.g.
    #      ['%pdf2img.py', '-pages=1', '-noAnnot', 'PDF2IMG.pdf', 'jpg']
    def __call__(self, argv=sys.argv):
        self._get_args(argv)
        image_response = self._get_response()
        if image_response: return self._save_image(image_response)
        sys.exit(str(image_response))

    def _get_args(self, argv):
        try:
            self._get_options(argv[1:-2])
            self._input_file = argv[-2]
            self._output_form = argv[-1]
        except Exception:
            sys.exit('syntax: %s [options] inputFile outputForm' % argv[0])
    def _get_options(self, argv):
        self._options = {}
        for arg in argv:
            if arg.startswith('-'):
                arg = arg[1:]
                option, value = arg.split('=') if '=' in arg else (arg, True)
                self._options[option] = value
    def _get_response(self):
        client = pdfclient.Client(self._api_key, self._version, self._base_url)
        request = client.make_request(request_type='image')
        with open(self._input_file, 'rb') as input:
            return request.post(input, self._output_form, **self._options)
    def _save_image(self, image_response):
        base_file_name = os.path.splitext(self._input_file)[0]
        image_file = '.'.join((base_file_name, self._output_form))
        with open(image_file, 'wb') as image:
            image.write(image_response.output)
        print('created: %s' % image_file)


if __name__ == '__main__':
    PDF2IMG('TODO: paste your API key here')()

