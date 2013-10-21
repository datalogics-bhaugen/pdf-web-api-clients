# Copyright (c) 2013, Datalogics, Inc. All rights reserved.

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

import sys
import inspect

import requests
import simplejson as json


## %Request factory
class Application(object):
    BASE_URL = 'https://pdfprocess.datalogics-cloud.com'
    ## @param id from our [developer portal](http://api.datalogics-cloud.com/)
    #  @param key from our [developer portal](http://api.datalogics-cloud.com/)
    def __init__(self, id, key):
        self._id, self._key = id, key

    def __str__(self):
        return json.dumps({'id': self.id, 'key': self.key})

    ## Create a request for the specified request type
    # @return a Request object
    # @param request_type e.g. 'render/pages'
    def make_request(self, request_type, base_url=BASE_URL):
        return Application._request_class(request_type)(self, base_url)

    @classmethod
    def _request_class_predicate(cls, request_type):
        return lambda m: inspect.isclass(m) and 'REQUEST_TYPE' in dir(m) \
            and m.REQUEST_TYPE == request_type
    @classmethod
    def _request_class(cls, request_type):
        is_request_class = cls._request_class_predicate(request_type)
        members = inspect.getmembers(sys.modules[__name__], is_request_class)
        return members[0][1]
    @property
    ## ID property (string)
    def id(self): return self._id
    @property
    ## Key property (string)
    def key(self): return self._key


## Service request
class Request(object):
    def __init__(self, application, base_url):
        self._data = {'application': str(application)}
        self._url = '{}/api/actions/{}'.format(base_url, self.REQUEST_TYPE)

    ## Send request
    #  @return a Response object
    #  @param input input document URL or file object
    #  @param input_name input name for service log
    #  @param password document password
    #  @param options other request options
    def __call__(self, input, input_name=None, password=None, options={}):
        data, files = self._data.copy(), None
        if password: data['password'] = password
        if options: data['options'] = json.dumps(options)
        string_types = (str, unicode) if sys.version_info.major < 3 else (str,)
        if type(input) in string_types:
            data['inputURL'] = input
        else:
            input.seek(0)
            files = {'input': input}
            data['inputName'] = input.name
        if input_name: data['inputName'] = input_name
        request_response =\
            requests.post(self.url, verify=False, data=data, files=files)
        return Response(request_response)

    @property
    ## %Request URL property (string)
    def url(self): return self._url


## Service response
class Response(object):
    def __init__(self, request_response):
        self._http_code = request_response.status_code
        self._error_code, self._error_message = None, None
        self._output = request_response.content if self else None
        if not self:
            try:
                json = request_response.json()
                self._error_code = json['errorCode']
                self._error_message = json['errorMessage']
            except:
                pass
    def __str__(self):
        return self.output or \
            '{}: {}'.format(self.error_code, self.error_message)
    def __bool__(self):
        return self.http_code == requests.codes.ok
    __nonzero__ = __bool__
    @property
    ## HTTP status code (int)
    def http_code(self): return self._http_code

    @property
    ## Document or image data (bytes) if request was successful, otherwise None
    def output(self): return self._output

    @property
    ## None if successful, otherwise API error code (int)
    def error_code(self): return self._error_code

    @property
    ## None if successful, otherwise information (string) about error
    def error_message(self): return self._error_message


## API error codes
class ErrorCode:
    AuthorizationError = 1
    InvalidSyntax = 2
    InvalidInput = 3
    InvalidPassword = 4
    MissingPassword = 5
    AdeptDRM = 6
    InvalidOutputFormat = 7
    InvalidPage = 8
    RequestTooLarge = 9
    UsageLimitExceeded = 10
    UnknownError = 20


## Flatten form fields and other annotations
class FlattenForm(Request):
    REQUEST_TYPE = 'flatten/form'
    ## Error codes for %FlattenForm requests
    class ErrorCode(ErrorCode):
        NoAnnotations = 21
    @property
    ## Output filename extension property (string)
    def output_format(self): return 'pdf'


## Create raster image representation
class RenderPages(Request):
    REQUEST_TYPE = 'render/pages'
    ## Error codes for %RenderPages requests
    class ErrorCode(ErrorCode):
        InvalidColorModel = 31
        InvalidCompression = 32
        InvalidRegion = 33
        InvalidResolution = 34
    @property
    ## Output filename extension property (string)
    def output_format(self): return self._output_format
    ## Send request
    #  @return a requests.Response object
    #  @param input input document URL or file object
    #  @param input_name input name for service log
    #  @param password document password
    #  @param options e.g. {'outputFormat': 'jpg', 'printPreview': True}
    #  * [colorModel](https://api.datalogics-cloud.com/docs#colorModel)
    #  * [compression](https://api.datalogics-cloud.com/docs#compression)
    #  * [disableColorManagement]
    #     (https://api.datalogics-cloud.com/docs#disableColorManagement)
    #  * [disableThinLineEnhancement]
    #     (https://api.datalogics-cloud.com/docs#disableThinLineEnhancement)
    #  * [imageHeight](https://api.datalogics-cloud.com/docs#imageHeight)
    #  * [imageWidth](https://api.datalogics-cloud.com/docs#imageWidth)
    #  * [OPP](https://api.datalogics-cloud.com/docs#OPP)
    #  * [outputFormat](https://api.datalogics-cloud.com/docs#outputFormat)
    #  * [pages](https://api.datalogics-cloud.com/docs#pages)
    #  * [password](https://api.datalogics-cloud.com/docs#password)
    #  * [pdfRegion](https://api.datalogics-cloud.com/docs#pdfRegion)
    #  * [printPreview](https://api.datalogics-cloud.com/docs#printPreview)
    #  * [resolution](https://api.datalogics-cloud.com/docs#resolution)
    #  * [smoothing](https://api.datalogics-cloud.com/docs#smoothing)
    #  * [suppressAnnotations]
    #     (https://api.datalogics-cloud.com/docs#suppressAnnotations)
    def __call__(self, input, input_name=None, password=None, options={}):
        self._output_format = options.get('outputFormat', 'png')
        return Request.__call__(self, input=input, input_name=input_name,
                                password=password, options=options)
