# Copyright (c) 2014, Datalogics, Inc. All rights reserved.

"Sample pdfprocess client module"

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

import inspect
import json
import os
import sys

import requests


## Service request factory:
#  construct this to create service requests
class Application(object):
    BASE_URL = 'https://pdfprocess.datalogics.com'
    ## @param id from our [developer portal](http://api.datalogics-cloud.com/)
    #  @param key from our [developer portal](http://api.datalogics-cloud.com/)
    def __init__(self, id, key):
        self._json = json.dumps({'id': id, 'key': key})

    ## Create a request for the specified request type
    # @return a Request object
    # @param request_type e.g. 'FlattenForm'
    def make_request(self, request_type, base_url=BASE_URL):
        return Application._request_class(request_type)(self._json, base_url)

    @classmethod
    def _request_class(cls, request_type):
        is_request_class =\
            lambda m: inspect.isclass(m) and m.__name__ == request_type
        members = inspect.getmembers(sys.modules[__name__], is_request_class)
        return members[0][1]


## Service request (base class):
#  uses <a href="http://docs.python-requests.org/en/latest/">Requests</a>
#  to post request
class Request(object):
    INPUT_TYPES = {}
    def __init__(self, application_json, base_url, url_suffix):
        self._application = application_json
        self._url = '{}/api/actions/{}'.format(base_url, url_suffix)

    ## Send request
    #  @return a Response object
    #  @param files dict of input file objects
    #  @param data dict with keys in
    #   ('inputURL', 'inputName', 'password', 'options')
    def __call__(self, files, **data):
        data = data.copy()
        data['application'] = self._application
        for file in files.values(): file.seek(0)
        if 'inputName' not in data:
            if 'input' in files and 'name' in dir(files['input']):
                data['inputName'] = files['input'].name
        if 'options' in data:
            for option in data['options']:
                if option not in self.OPTIONS:
                    raise Exception('invalid option: {}'.format(option))
            data['options'] = json.dumps(data['options'])
        return Response(requests.post(self._url, files=files, data=data))

    def part_name(self, filename):
        data_format = os.path.splitext(filename)[1][1:].upper()
        for key in self.INPUT_TYPES.keys():
            if data_format == key or data_format in key:
                return self.INPUT_TYPES[key]


## Service response
class Response(object):
    def __init__(self, request_response):
        self._response = request_response
        self._error_code, self._error_message = None, None
        if not self.ok: self._not_ok()
    def __str__(self):
        if self.output:
            return self.output
        if self.error_code:
            return '{}: {}'.format(self.error_code, self.error_message)
        return 'HTTP: {}'.format(self.http_code)
    def __getattr__(self, name):
        return getattr(self._response, name)
    def _not_ok(self):
        try:
            json = self._response.json()
            self._error_code = json['errorCode']
            self._error_message = json['errorMessage']
        except:
            pass  # 404?
    @property
    ## True only if http_code is 200
    def ok(self): return self.http_code == requests.codes.ok
    @property
    ## HTTP status code (int)
    def http_code(self): return self._response.status_code
    @property
    ## Document, form, or image data (bytes) if request was successful,
    #  otherwise None
    def output(self): return self._response.content if self.ok else None
    @property
    ## None if successful, otherwise API
    #   [error code]
    #    (https://api.datalogics-cloud.com/Getting-Started#ErrorMessages)
    #    (int)
    def error_code(self): return self._error_code
    @property
    ## None if successful, otherwise an
    #   [error message]
    #    (https://api.datalogics-cloud.com/Getting-Started#ErrorMessages)
    #    (string)
    def error_message(self): return self._error_message


## API error codes
class ErrorCode:
    AuthorizationError = 1
    InvalidSyntax = 2
    InvalidInput = 3
    InvalidPassword = 4
    MissingPassword = 5
    UnsupportedSecurityProtocol = 6
    InvalidOutputFormat = 7
    InvalidPage = 8
    RequestTooLarge = 9
    UsageLimitExceeded = 10
    UnknownError = 20

## Service request (add images to a PDF)
class AddImages(Request):
    INPUT_TYPES = {'JSON': 'imageSettings',
                   ('BMP', 'GIF', 'JPG'): 'resource[{}]'}
    ## %AddImages has no request options
    OPTIONS = []
    ## Error codes for %AddImages requests
    class ErrorCode(ErrorCode):
        pass
    def __init__(self, application, base_url):
        Request.__init__(self, application, base_url, 'add/images')

## Service request (decorate with supplied header/footer, watermark,
#  and background data)
class DecorateDocument(Request):
    INPUT_TYPES = {'JSON': 'decorationData',
                   'XML': 'decorationData[{}]',
                   'MF': 'manifest',
                   ('BMP', 'GIF', 'JPG', 'PDF'): 'resource[{}]'}
    ## %DecorateDocument has no request options
    OPTIONS = []
    ## Error codes for %DecorateDocument requests
    class ErrorCode(ErrorCode):
        pass
    def __init__(self, application, base_url):
        Request.__init__(self, application, base_url, 'decorate/document')

## Service request (export FDF, XFDF, or XML form data)
class ExportFormData(Request):
    ## %ExportFormData options:
    #  * [exportXFDF]
    #     (https://api.datalogics-cloud.com/docs#exportXFDF)
    #     export XFDF instead of FDF for AcroForm input
    OPTIONS = ['exportXFDF']
    ## Error codes for %ExportFormData requests
    class ErrorCode(ErrorCode):
        ExportXFDFFromXFA = 41
    def __init__(self, application, base_url):
        Request.__init__(self, application, base_url, 'export/form-data')


## Service request (fill form fields with supplied data)
class FillForm(Request):
    INPUT_TYPES = {('CSV', 'FDF', 'JSON', 'TSV', 'XFDF', 'XML'): 'formsData'}
    ## %FillForm request options:
    #  * [disableCalculation]
    #     (https://api.datalogics-cloud.com/docs#disableCalculation)
    #     do not run calculations afterward
    #  * [disableGeneration]
    #     (https://api.datalogics-cloud.com/docs#disableGeneration):
    #     do not generate appearances afterward
    #  * [flatten](https://api.datalogics-cloud.com/docs#flatten):
    #     flatten form afterward
    OPTIONS = ['disableCalculation', 'disableGeneration', 'flatten']
    ## Error codes for %FillForm requests
    class ErrorCode(ErrorCode):
        pass
    def __init__(self, application, base_url):
        Request.__init__(self, application, base_url, 'fill/form')


## Service request (flatten form fields)
class FlattenForm(Request):
    ## %FlattenForm has no request options
    OPTIONS = []
    ## Error codes for %FlattenForm requests
    class ErrorCode(ErrorCode):
        NoAnnotations = 21
    def __init__(self, application, base_url):
        Request.__init__(self, application, base_url, 'flatten/form')


## Service request (create raster image representation)
class RenderPages(Request):
    ## %RenderPages request options:
    #  * [colorModel](https://api.datalogics-cloud.com/docs#colorModel):
    #     rgb (default), gray, rgba, cmyk, or lab
    #  * [compression](https://api.datalogics-cloud.com/docs#compression):
    #     lzw (default), g3, g4, or jpg
    #  * [disableColorManagement]
    #     (https://api.datalogics-cloud.com/docs#disableColorManagement):
    #     for downstream color management (rarely used)
    #  * [disableThinLineEnhancement]
    #     (https://api.datalogics-cloud.com/docs#disableThinLineEnhancement)
    #     for high-resolution output (rarely used)
    #  * [imageHeight](https://api.datalogics-cloud.com/docs#imageHeight):
    #     pixels
    #  * [imageWidth](https://api.datalogics-cloud.com/docs#imageWidth):
    #     pixels
    #  * [OPP](https://api.datalogics-cloud.com/docs#OPP): overprint preview
    #  * [outputFormat](https://api.datalogics-cloud.com/docs#outputFormat):
    #     png (default), bmp, gif, jpg, or tif
    #  * [pages](https://api.datalogics-cloud.com/docs#pages):
    #     default = 1
    #  * [pdfRegion](https://api.datalogics-cloud.com/docs#pdfRegion):
    #     crop (default), art, bleed, bounding, media, or trim
    #  * [printPreview](https://api.datalogics-cloud.com/docs#printPreview):
    #     ignored if suppressAnnotations is true
    #  * [resampler](https://api.datalogics-cloud.com/docs#resampler):
    #     auto (default), bicubic, none
    #  * [resolution](https://api.datalogics-cloud.com/docs#resolution):
    #     12 to 2400 (default = 150)
    #  * [smoothing](https://api.datalogics-cloud.com/docs#smoothing):
    #     all (default), none, text, line, image, or comma-separated value
    #  * [suppressAnnotations]
    #     (https://api.datalogics-cloud.com/docs#suppressAnnotations):
    #     draw only actual page contents
    OPTIONS = ['colorModel', 'compression',
               'disableColorManagement', 'disableThinLineEnhancement',
               'imageHeight', 'imageWidth',
               'OPP', 'outputFormat',
               'pages', 'pdfRegion',
               'printPreview', 'resampler',
               'resolution', 'smoothing',
               'suppressAnnotations']
    ## Error codes for %RenderPages requests
    class ErrorCode(ErrorCode):
        InvalidColorModel = 31
        InvalidCompression = 32
        InvalidRegion = 33
        InvalidResolution = 34
    def __init__(self, application, base_url):
        Request.__init__(self, application, base_url, 'render/pages')

## Service request (retrieve PDF document properties)
class RetrieveDocumentProperties(Request):
    ## %RetrieveDocumentProperties has no request options
    OPTIONS = []
    ## Error codes for %RetrieveDocumentProperties requests
    class ErrorCode(ErrorCode):
        pass
    def __init__(self, application, base_url):
        Request.__init__(self, application, base_url,
                         'retrieve/document/properties')
