#!/usr/bin/env python

# Copyright (c) 2013, Datalogics, Inc. All rights reserved.

"Sample pdfclient driver"

# This agreement is between Datalogics, Inc. 101 N. Wacker Drive, Suite 1800,
# Chicago, IL 60606 ("Datalogics") and you, an end user who downloads source
# code examples for integrating to the Datalogics (R) PDF Web API (TM)
# ("the Example Code"). By accepting this agreement you agree to be bound
# by the following terms of use for the Example Code.
#
# LICENSE
# -------
# Datalogics hereby grants you a royalty-free, non-exclusive license to
# download and use the Example Code for any lawful purpose. There is no charge
# for use of Example Code.
#
# OWNERSHIP
# ---------
# The Example Code and any related documentation and trademarks are and shall
# remain the sole and exclusive property of Datalogics and are protected by
# the laws of copyright in the U.S. and other countries.
#
# Datalogics and Datalogics PDF Web API are trademarks of Datalogics, Inc.
#
# TERM
# ----
# This license is effective until terminated. You may terminate it at any
# other time by destroying the Example Code.
#
# WARRANTY DISCLAIMER
# -------------------
# THE EXAMPLE CODE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER
# EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
# DATALOGICS DISCLAIM ALL OTHER WARRANTIES, CONDITIONS, UNDERTAKINGS OR
# TERMS OF ANY KIND, EXPRESS OR IMPLIED, WRITTEN OR ORAL, BY OPERATION OF
# LAW, ARISING BY STATUTE, COURSE OF DEALING, USAGE OF TRADE OR OTHERWISE,
# INCLUDING, WARRANTIES OR CONDITIONS OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE, SATISFACTORY QUALITY, LACK OF VIRUSES, TITLE,
# NON-INFRINGEMENT, ACCURACY OR COMPLETENESS OF RESPONSES, RESULTS, AND/OR
# LACK OF WORKMANLIKE EFFORT. THE PROVISIONS OF THIS SECTION SET FORTH
# SUBLICENSEE'S SOLE REMEDY AND DATALOGICS'S SOLE LIABILITY WITH RESPECT
# TO THE WARRANTY SET FORTH HEREIN. NO REPRESENTATION OR OTHER AFFIRMATION
# OF FACT, INCLUDING STATEMENTS REGARDING PERFORMANCE OF THE EXAMPLE CODE,
# WHICH IS NOT CONTAINED IN THIS AGREEMENT, SHALL BE BINDING ON DATALOGICS.
# NEITHER DATALOGICS WARRANT AGAINST ANY BUG, ERROR, OMISSION, DEFECT,
# DEFICIENCY, OR NONCONFORMITY IN ANY EXAMPLE CODE.

import os
import sys

from pdfclient import Application, ImageRequest


## Returned by PDF2IMG.__call__
class Response(object):
    def __init__(self, pdf2img, image_response):
        base_filename = os.path.splitext(pdf2img.input_filename)[0]
        self._image_filename = '.'.join((base_filename, pdf2img.output_form))
        self._image_response = image_response
    def __str__(self):
        return str(self._image_response)
    def __bool__(self):
        return bool(self._image_response)
    __nonzero__ = __bool__
    def __getattr__(self, key):
        return getattr(self._image_response, key)
    ## Create #image_filename
    def save_image(self):
        with open(self.image_filename, 'wb') as image_file:
            image_file.write(self.output)

    @property
    ## Image filename
    def image_filename(self):
        if self: return self._image_filename


## Sample pdfclient driver
class PDF2IMG(Application):
    ## @param version e.g. Application.VERSION
    #  @param base_url e.g. Application.BASE_URL
    #  @param argv e.g.
    #      ['%pdf2img.py', '-outputForm=jpg', '-printPreview', 'PDF2IMG.pdf']
    def __call__(self, version, base_url, argv):
        self._initialize(argv)
        request = ImageRequest(self, version, base_url)
        with open(self._input_filename, 'rb') as input_file:
            return Response(self,
                request.post(input_file, **self.options))

    def _initialize(self, argv):
        try:
            self._parse_args(argv)
        except Exception:
            sys.exit('syntax: %s [options] inputFile' % argv[0])
        self._image_filename = None
    def _parse_args(self, argv):
        self._output_form = 'tif'
        self._set_options(argv[1:-1])
        self._input_filename = argv[-1]
    def _set_options(self, argv):
        self._options = {}
        for arg in argv:
            if not arg.startswith('-'): sys.exit('syntax error: %s' % argv)
            arg = arg[1:]
            option, value = arg.split('=') if '=' in arg else (arg, True)
            self._options[option] = value
            if option.lower() == 'outputform':
                self._output_form = value
    @property
    ## Input filename passed to __call__
    def input_filename(self): return self._input_filename
    @property
    ## Output form passed to __call__, e.g. 'jpg'
    def output_form(self): return self._output_form
    @property
    ## Options passed to __call__ (dict)
    def options(self): return self._options


def run(argv):
    pdf2img = PDF2IMG('TODO: Application ID', 'TODO: Application key')
    return pdf2img(Application.VERSION, Application.BASE_URL, argv)

if __name__ == '__main__':
    response = run(sys.argv)
    if response:
        response.save_image()
        print('created: %s' % response.image_filename)
    else:
        print(response)

