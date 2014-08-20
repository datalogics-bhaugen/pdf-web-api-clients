#!/usr/bin/env python

# Copyright (c) 2014, Datalogics, Inc. All rights reserved.

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
import platform
import sys

import pdfclient


APPLICATION_ID = 'your app id'  # TODO: paste!
APPLICATION_KEY = 'your app key'  # TODO: paste!

if platform.system() == 'Windows':
    JSON = '"{{\\"printPreview\\": true, \\"outputFormat\\": \\"jpg\\"}}"'
else:
    JSON = "'{{\"printPreview\": true, \"outputFormat\": \"jpg\"}}'"

OPTIONS = ('inputName', 'password', 'options')
PDF2IMG_GUIDE = 'http://www.datalogics.com/pdf/doc/pdf2img.pdf'
USAGE_OPTIONS = '[{}=name] [{}=pwd] [{}=json]'.format(*OPTIONS)
USAGE = 'usage: {0} request_type <input document> [input file(s)] ' +\
        USAGE_OPTIONS + '\n' +\
        'example: {0} DecorateDocument any.pdf headers.xml\n' +\
        'example: {0} DecorateDocument any.pdf watermarks.json\n' +\
        'example: {0} FillForm form.pdf form.fdf\n' +\
        'example: {0} FlattenForm hello_world.pdf\n' +\
        'example: {0} RenderPages ' + PDF2IMG_GUIDE + ' options=' + JSON


## Sample pdfclient driver:
#  execute pdfprocess.py with no arguments for usage information
class Client(pdfclient.Application):
    ## Create a pdfclient.Request from command-line arguments and execute it
    #  @return a Response object
    #  @param args e.g.['%pdfprocess.py', 'FlattenForm', 'hello_world.pdf']
    #  @param base_url
    def __call__(self, args, base_url=pdfclient.Application.BASE_URL):
        parser = self._parse(args, base_url)
        api_response = self._request(parser.files, **parser.data)
        return Response(api_response, self.output_format)

    def _parse(self, args, base_url):
        if len(args) > 2:
            try:
                self._request = self.make_request(args[1], base_url)
                return Parser(self._request, args[2:])
            except Exception as exception:
                print(exception)
        sys.exit(USAGE.format(args[0]))
    @property
    def output_format(self):
        return self._request.output_format


## #pdfclient.Response wrapper saves output to a file
class Response(object):
    def __init__(self, response, output_format):
        self._response, self._output_format = response, output_format
    def __str__(self):
        return str(self._response)
    def __getattr__(self, key):
        return getattr(self._response, key)
    ## Save output in file named #output_filename
    def save_output(self):
        with open(self.output_filename, 'wb') as output:
            output.write(self.output)

    def output_format(self):
        if self.output.startswith('%FDF'): return 'fdf'
        xml_tag = '<?xml version="1.0" encoding="UTF-8"?>'
        if self.output.startswith(xml_tag + '<xfdf xmlns'): return 'xfdf'
        if self.output.startswith(xml_tag + '<xfa:datasets'): return 'xml'
    @property
    ## True only if request succeeded
    def ok(self):
        return self._response.ok
    @property
    def output_filename(self):
        if self.ok and not self._output_format:
            self._output_format = self.output_format()
        if self._output_format:
            return 'pdfprocess.{}'.format(self._output_format)
        return 'pdfprocess.out'


## Translate command line arguments and open input files for
#  <a href="http://docs.python-requests.org/en/latest/">Requests</a>
class Parser(object):
    def __init__(self, request, args):
        self._data, self._files = {}, {}
        files = [arg for arg in args if '=' not in arg]
        options = [arg.split('=') for arg in args if arg not in files]
        urls = [file for file in files if Parser._is_url(file)]
        if len(urls) > 1:
            raise Exception('invalid input: {} URLs'.format(len(urls)))
        if urls:
            files.remove(urls[0])
            self.data['inputURL'] = urls[0]
        else:
            self.files['input'] = open(files[0], 'rb')
        for option, value in options:
            if option not in OPTIONS:
                raise Exception('invalid option: {}'.format(option))
            self.data[option] =\
                json.loads(value) if option == 'options' else value
        suffixes = {}
        for file in files[1:]:
            part_name = request.part_name(file)
            if isinstance(part_name, list):
                part_name = part_name[0]
                suffixes[part_name] = suffixes.get(part_name, -1) + 1
                part_name = '{}[{}]'.format(part_name, suffixes[part_name])
            self.files[part_name] = open(file, 'rb')
    def __del__(self):
        for file in self.files.values():
            file.close()
    @classmethod
    def _is_url(cls, filename):
        name = filename.lower()
        if name.startswith('http://') or name.startswith('https://'):
            return filename
    @property
    ## form parts that will be passed to requests.post
    def data(self): return self._data
    @property
    ## files that will be passed to requests.post
    def files(self): return self._files


def run(args, app_id=APPLICATION_ID, app_key=APPLICATION_KEY):
    return Client(app_id, app_key)(args)

if __name__ == '__main__':
    response = run(sys.argv)
    if response.ok:
        response.save_output()
        print('created: {}'.format(response.output_filename))
    else:
        print(response)
