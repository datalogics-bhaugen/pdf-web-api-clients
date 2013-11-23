#!/usr/bin/env python

# Copyright (c) 2013, Datalogics, Inc. All rights reserved.

"Sample pdfclient driver"

# This agreement is between Datalogics, Inc. 101 N. Wacker Drive, Suite 1800,
# Chicago, IL 60606 ("Datalogics") and you, an end user who downloads
# source code examples for integrating to the Datalogics (R) PDF WebAPI (TM)
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
# Datalogics and Datalogics PDF WebAPI are trademarks of Datalogics, Inc.
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

import json
import os
import re
import sys

from pdfclient import Application


APPLICATION_ID = 'your app id'  # TODO: paste!
APPLICATION_KEY = 'your app key'  # TODO: paste!

JSON_OPTIONS = ('options',)
OPTIONS = ('inputName', 'password') + JSON_OPTIONS
PDF2IMG_GUIDE = 'http://www.datalogics.com/pdf/doc/pdf2img.pdf'
USAGE_OPTIONS = '[{}=name] [{}=pwd] [{}=json]'.format(*OPTIONS)
USAGE = 'usage: {0} request_type input ' + USAGE_OPTIONS + '\n' +\
        'example: {0} FlattenForm hello_world.pdf\n' +\
        'example: {0} RenderPages ' + PDF2IMG_GUIDE +\
        ' options={{"printPreview": True, "outputFormat": "jpg"}}'


## Sample pdfclient driver:
#  execute pdfprocess.py with no arguments for usage information
class Client(Application):
    ## Create a pdfclient.Request from command-line arguments and execute it
    #  @return a Response object
    #  @param args e.g.['%pdfprocess.py', 'FlattenForm', 'hello_world.pdf']
    #  @param base_url
    def __call__(self, args, base_url=Application.BASE_URL):
        if len(args) < 3: self._exit(args)
        input, data = self._initialize(args)
        url_input = re.match('http:|https:', input.lower())
        self._api_request = self.make_request(args[1], base_url)
        input_name = os.path.basename(input) if url_input else input
        self._input_name = data.get('inputName', input_name)
        send_method = self._send_url if url_input else self._send_file
        return Response(send_method(input, data), self.output_filename)

    def _exit(self, args):
        sys.exit(USAGE.format(args[0]))
    def _initialize(self, args):
        try:
            return args[2], self._parse_args(args[3:])
        except Exception as exception:
            print(exception)
            self._exit(args)
    def _parse_args(self, args):
        result = {}
        for arg in args:
            option, value = arg.split('=')
            if option not in OPTIONS:
                raise Exception('invalid option: {}'.format(option))
            json_option = option in JSON_OPTIONS
            result[option] = json.loads(value) if json_option else value
        return result
    def _send_file(self, input, data):
        with open(input, 'rb') as input_file:
            return self._api_request(input_file, **data)
    def _send_url(self, input, data):
        return self._api_request(input, **data)
    @property
    ## Derived from the input name or explicitly specified
    def input_name(self):
        return self._input_name
    @property
    ## #input_name with extension replaced by requested output format
    def output_filename(self):
        input_name = os.path.splitext(self._input_name)[0]
        return '{}.{}'.format(input_name, self._api_request.output_format)


## #pdfclient.Response wrapper
#  saves output to the file specified by the request
class Response(object):
    def __init__(self, response, output_filename):
        self._response, self._output_filename = response, output_filename
    def __str__(self):
        return str(self._response)
    def __getattr__(self, key):
        return getattr(self._response, key)
    ## Save output in file named #output_filename
    def save_output(self):
        with open(self.output_filename, 'wb') as output:
            output.write(self.output)

    @property
    ## True only if request succeeded
    def ok(self):
        return self._response.ok
    @property
    ## Derived from Client.input_name and requested output format
    def output_filename(self):
        if self.ok: return self._output_filename


def run(args, app_id=APPLICATION_ID, app_key=APPLICATION_KEY):
    return Client(app_id, app_key)(args)

if __name__ == '__main__':
    response = run(sys.argv)
    if response.ok:
        response.save_output()
        print('created: {}'.format(response.output_filename))
    else:
        print(response)
