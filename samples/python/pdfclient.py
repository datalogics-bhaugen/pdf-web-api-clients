# Copyright (c) 2013, Datalogics, Inc. All rights reserved.

"Sample pdfprocess client module"

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

import base64
import sys

import requests
import simplejson as json


class Application(object):
    BASE_URL = 'https://pdfprocess.datalogics-cloud.com'
    VERSION = 0

    ## @param id from [3scale](http://api.datalogics-cloud.com/)
    #  @param key from [3scale](http://api.datalogics-cloud.com/)
    def __init__(self, id, key):
        self._id, self._key = (id, key)
    def __str__(self):
        return json.dumps({'id': self.id, 'key': self.key})

    ## Request factory
    # @return a Request object
    # @param request_type e.g. 'image'
    def make_request(self, request_type, version=VERSION, base_url=BASE_URL):
        if request_type == 'image':
            return ImageRequest(self, version, base_url)

    @property
    ## ID property (string)
    def id(self): return self._id
    @property
    ## Key property (string)
    def key(self): return self._key


class Request(object):
    def __init__(self, application, request_type, version, base_url):
        self._application = {'application': str(application)}
        self._url = '%s/api/%s/actions/%s' % (base_url, version, request_type)

    ## Send POST request with input file
    #  @return a requests.Response object
    #  @param input input document file object
    #  @param options e.g. {'outputForm': 'jpg', 'printPreview': True}
    def post_file(self, input, options={}):
        self._reset(options)
        files = {'input': input}
        if input.name: self.data['inputName'] = input.name
        return \
            requests.post(self.url, data=self.data, files=files, verify=False)

    ## Send POST request with input URL
    #  @return a requests.Response object
    #  @param input_url input document URL
    #  @param options e.g. {'outputForm': 'jpg', 'printPreview': True}
    def post_url(self, input_url, options={}):
        self._reset(options)
        self.data['inputURL'] = input_url
        return requests.post(self.url, data=self.data, verify=False)
    def _reset(self, options):
        self._data = self._application.copy()
        if options: self.data['options'] = json.dumps(options)
    @property
    ## %Request data property (dict), set by #post_file or #post_url
    def data(self): return self._data
    @property
    ## %Request URL property (string)
    def url(self): return self._url


class ImageRequest(Request):
    def __init__(self, application, version, base_url):
        Request.__init__(self, application, 'image', version, base_url)

    ## Send POST request with input file
    #  @return an ImageResponse object
    #  @param input input document file object
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
    def post_file(self, input, options={}):
        return ImageResponse(Request.post_file(self, input, options))

    ## Send POST request with input URL
    #  @return an ImageResponse object
    #  @param input_url input document URL
    #  @param options see #post_file
    def post_url(self, input_url, options={}):
        return ImageResponse(Request.post_url(self, input_url, options))


## Returned by Request.post_file and Request.post_url
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
    ## Base64-encoded data (string) if request was successful, otherwise None
    def output(self):
        if 'output' in self._json and self: return self['output']

    @property
    ## None if successful, otherwise information (string) about process_code
    def exc_info(self):
        if 'output' in self._json and not self: return self['output']

    @property
    ## HTTP status code (int)
    def status_code(self): return self._status_code


## Returned by ImageRequest.post_file and ImageRequest.post_url
class ImageResponse(Response):
    def _image(self):
        if sys.version_info.major < 3:
            return self['output'].decode('base64')
        else:
            return base64.b64decode(self['output'])
    @property
    ## Image data (bytes) if request was successful, otherwise None
    def output(self):
        if self: return self._image()


## Values returned by Response.process_code
class ProcessCode:
    OK = 0
    AuthorizationError = 1
    InvalidSyntax = 2
    InvalidInput = 3
    InvalidPassword = 4
    MissingPassword = 5
    AdeptDRM = 6
    InvalidOutputType = 7
    InvalidPage = 8
    RequestTooLarge = 9
    UsageLimitExceeded = 10
    UnknownError = 20

## Values returned by ImageResponse.process_code
class ImageProcessCode(ProcessCode):
    InvalidColorModel = 21
    InvalidCompression = 22
    InvalidRegion = 23
    InvalidResolution = 24
