#!/usr/bin/env python

# Copyright (c) 2013, Datalogics, Inc. All rights reserved.

# TODO: sample disclaimer

"Sample pdfclient driver"

import os
import sys

import pdfclient


## Returned by PDF2IMG.__call__
class Response(object):
    def __init__(self, pdf2img, image_response):
        base_file_name = os.path.splitext(pdf2img.input_file)[0]
        self._image_file = '.'.join((base_file_name, pdf2img.output_form))
        self._image_response = image_response
    def __bool__(self):
        return bool(self._image_response)
    __nonzero__ = __bool__
    def __getattr__(self, key):
        return getattr(self._image_response, key)
    ## Create #image_file
    def save_image(self):
        with open(self.image_file, 'wb') as image:
            image.write(self.output)

    @property
    ## Image filename
    def image_file(self):
        if self: return self._image_file


## Sample pdfclient driver
class PDF2IMG(pdfclient.Client):
    ## @param argv e.g.
    #      ['%pdf2img.py', '-pages=1', '-printPreview', 'PDF2IMG.pdf', 'jpg']
    def __call__(self, argv):
        self._initialize(argv)
        request = pdfclient.ImageRequest(self)
        with open(self._input_file, 'rb') as input:
            return Response(self,
                request.post(input, self.output_form, **self.options))

    def _initialize(self, argv):
        try:
            self._parse_args(argv)
        except Exception:
            sys.exit('syntax: %s [options] inputFile outputForm' % argv[0])
        self._image_file = None
    def _parse_args(self, argv):
        self._set_options(argv[1:-2])
        self._input_file = argv[-2]
        self._output_form = argv[-1]
    def _set_options(self, argv):
        self._options = {}
        for arg in argv:
            if arg.startswith('-'):
                arg = arg[1:]
                option, value = arg.split('=') if '=' in arg else (arg, True)
                self._options[option] = value
    @property
    ## Input filename passed to __call__
    def input_file(self): return self._input_file
    @property
    ## Output form passed to __call__, e.g. 'jpg'
    def output_form(self): return self._output_form
    @property
    ## Options passed to __call__ (dict)
    def options(self): return self._options


if __name__ == '__main__':
    pdf2img = PDF2IMG('TODO: paste your API key here')
    response = pdf2img(sys.argv)
    if not response: sys.exit(response)
    response.save_image()
    print('created: %s' % response.image_file)

