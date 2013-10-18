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
import base64
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
        self._url = '%s/api/actions/%s' % (base_url, self.REQUEST_TYPE)

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
        self._status_code = request_response.status_code
        try: self._json = request_response.json()
        except ValueError: self._json = {}
    def __str__(self):
        return '%s: %s' % (self.process_code, self.output or self.exc_info)
    def __bool__(self):
        return self.process_code == 0
    __nonzero__ = __bool__
    def __getitem__(self, key):
        return json.dumps(self._json[key])
    @property
    ## API status code (int)
    def process_code(self):
        if 'processCode' in self._json: return int(self['processCode'])

    @property
    ## Document or image data (bytes) if request was successful, otherwise None
    def output(self):
        if 'output' not in self._json or not self:
            return None
        elif sys.version_info.major < 3:
            return self['output'].decode('base64')
        else:
            return base64.b64decode(self['output'])

    @property
    ## None if successful, otherwise information (string) about process_code
    def exc_info(self):
        if 'output' in self._json and not self: return self['output']

    @property
    ## HTTP status code (int)
    def status_code(self): return self._status_code


## API status codes
class ProcessCode:
    OK = 0
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
    ## Status codes for %FlattenForm requests
    class ProcessCode(ProcessCode):
        NoAnnotations = 21
    @property
    ## Output filename extension property (string)
    def output_format(self): return 'pdf'


## Create raster image representation
class RenderPages(Request):
    REQUEST_TYPE = 'render/pages'
    ## Status codes for %RenderPages requests
    class ProcessCode(ProcessCode):
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
    #  @param options e.g. {'outputForm': 'jpg', 'printPreview': True}
    #  * [colorModel](https://api.datalogics-cloud.com/docs#colorModel)
    #  * [compression](https://api.datalogics-cloud.com/docs#compression)
    #  * [disableColorManagement]
    #     (https://api.datalogics-cloud.com/docs#disableColorManagement)
    #  * [disableThinLineEnhancement]
    #     (https://api.datalogics-cloud.com/docs#disableThinLineEnhancement)
    #  * [imageHeight](https://api.datalogics-cloud.com/docs#imageHeight)
    #  * [imageWidth](https://api.datalogics-cloud.com/docs#imageWidth)
    #  * [OPP](https://api.datalogics-cloud.com/docs#OPP)
    #  * [outputForm](https://api.datalogics-cloud.com/docs#outputForm)
    #  * [pages](https://api.datalogics-cloud.com/docs#pages)
    #  * [password](https://api.datalogics-cloud.com/docs#password)
    #  * [pdfRegion](https://api.datalogics-cloud.com/docs#pdfRegion)
    #  * [printPreview](https://api.datalogics-cloud.com/docs#printPreview)
    #  * [resolution](https://api.datalogics-cloud.com/docs#resolution)
    #  * [smoothing](https://api.datalogics-cloud.com/docs#smoothing)
    #  * [suppressAnnotations]
    #     (https://api.datalogics-cloud.com/docs#suppressAnnotations)
    def __call__(self, input, input_name=None, password=None, options={}):
        self._output_format = options.get('outputForm', 'tif')
        return Request.__call__(self, input=input, input_name=input_name,
                                password=password, options=options)
