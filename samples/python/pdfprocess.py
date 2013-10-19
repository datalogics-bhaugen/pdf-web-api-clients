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

import os
import sys
import simplejson as json

from pdfclient import Application


OPTIONS = ('input_name', 'password', 'options')
USAGE_OPTIONS = '[{}=name] [{}=pwd] [{}=json]'.format(*OPTIONS)
USAGE = 'usage: {} requestType input ' + USAGE_OPTIONS


## Sample pdfclient driver
class Client(Application):
    ## @param argv e.g.['%pdfprocess.py', 'render/pages', 'hello_world.pdf']
    #  @param base_url
    def __call__(self, argv, base_url=Application.BASE_URL):
        args, input = self._initialize(argv), argv[2]
        self._request = self.make_request(argv[1], base_url)
        url_input = input.lower().startswith('http')
        input_name = os.path.basename(input) if url_input else input
        self._input_name = args.get('input_name', input_name)
        send_method = self._send_url if url_input else self._send_file
        return Response(send_method(input, args), self.output_filename)

    def _initialize(self, argv):
        try:
            return self._parse_args(argv)
        except Exception:
            sys.exit(USAGE.format(argv[0]))
    def _parse_args(self, argv):
        result = {}
        for arg in argv[3:]:
            option, value = arg.split('=')
            if option not in OPTIONS:
                raise Exception('invalid option: {}'.format(option))
            if option == 'options': value = json.loads(value)
            result[option] = value
        return result
    def _send_file(self, input, args):
        with open(input, 'rb') as input_file:
            return self._request(input_file, **args)
    def _send_url(self, input, args):
        return self._request(input, **args)
    @property
    ## Output filename
    def output_filename(self):
        input_name = os.path.splitext(self._input_name)[0]
        return '{}.{}'.format(input_name, self._request.output_format)


## #pdfclient.Response wrapper
class Response(object):
    def __init__(self, response, output_filename):
        self._response, self._output_filename = response, output_filename
    def __str__(self):
        return str(self._response)
    def __bool__(self):
        return bool(self._response)
    __nonzero__ = __bool__
    def __getattr__(self, key):
        return getattr(self._response, key)
    ## Save output in file named #output_filename
    def save_output(self):
        with open(self.output_filename, 'wb') as output:
            output.write(self.output)

    @property
    ## Output filename
    def output_filename(self):
        if self: return self._output_filename


def run(argv, app_id='TODO: Application ID', app_key='TODO: Application key'):
    return Client(app_id, app_key)(argv, Application.BASE_URL)

if __name__ == '__main__':
    response = run(sys.argv)
    if response:
        response.save_output()
        print('created: {}'.format(response.output_filename))
    else:
        print(response)
