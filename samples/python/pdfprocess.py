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
import sys

import pdfclient


APPLICATION_ID = 'your app id'  # TODO: paste!
APPLICATION_KEY = 'your app key'  # TODO: paste!

OPTIONS = ('inputName', 'password', 'options')
PDF2IMG_GUIDE = 'http://www.datalogics.com/pdf/doc/pdf2img.pdf'
USAGE_OPTIONS = '[{}=name] [{}=pwd] [{}=json]'.format(*OPTIONS)
USAGE = 'usage: {0} request_type input ' + USAGE_OPTIONS + '\n' +\
        'example: {0} FlattenForm hello_world.pdf\n' +\
        'example: {0} RenderPages ' + PDF2IMG_GUIDE +\
        ' options={{"printPreview": True, "outputFormat": "jpg"}}'


## Translate command line arguments to form needed by Client
class Parser(object):
    PART_NAME_FILE_FORMATS = {'formsData': ('FDF', 'XFDF')}
    def __init__(self, args):
        self._data, self._files = {}, {}
        files = [arg for arg in args if '=' not in arg]
        options = [arg.split('=') for arg in args if arg not in files]
        urls = [file for file in files if Parser._is_url(file)]
        if len(urls) > 1:
            raise Exception('invalid input: {} URLs'.format(len(urls)))
        if urls:
            files.remove(urls[0])
            self.data['inputURL'] = urls[0]
        for option, value in options:
            if option not in OPTIONS:
                raise Exception('invalid option: {}'.format(option))
            self.data[option] =\
                json.loads(value) if option == 'options' else value
        for file in files:
            self.files[Parser._part_name(file)] = open(file, 'rb')
    def __del__(self):
        for file in self.files.values():
            file.close()
    @classmethod
    def _is_url(cls, filename):
        name = filename.lower()
        if name.startswith('http://') or name.startswith('https://'):
            return filename
    @classmethod
    def _part_name(cls, filename):
        data_format = os.path.splitext(filename)[1][1:].upper()
        for part_name in Parser.PART_NAME_FILE_FORMATS:
            if data_format in Parser.PART_NAME_FILE_FORMATS[part_name]:
                return part_name
        return 'input'
    @property
    def data(self): return self._data
    @property
    def files(self): return self._files


## Sample pdfclient driver:
#  execute pdfprocess.py with no arguments for usage information
class Client(pdfclient.Application):
    ## Create a pdfclient.Request from command-line arguments and execute it
    #  @return a Response object
    #  @param args e.g.['%pdfprocess.py', 'FlattenForm', 'hello_world.pdf']
    #  @param base_url
    def __call__(self, args, base_url=pdfclient.Application.BASE_URL):
        parser = self._parse(args)
        input_url = parser.data.get('inputURL', '')
        input_name = os.path.basename(input_url) or parser.files['input'].name
        self._input_name = parser.data.get('inputName', input_name)
        self._api_request = self.make_request(args[1], base_url)
        api_response = self._api_request(parser.files, **parser.data)
        return Response(api_response, self.output_filename)

    def _parse(self, args):
        try:
            if len(args) > 2:
                return Parser(args[2:])
        except Exception as exception:
            print(exception)
        sys.exit(USAGE.format(args[0]))
    @property
    ## Derived from the input name or explicitly specified
    def input_name(self):
        return self._input_name
    @property
    ## #input_name with extension replaced by requested output format
    def output_filename(self):
        input_name = os.path.splitext(self.input_name)[0]
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
