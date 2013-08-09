# Copyright (c) 2013, Datalogics, Inc. All rights reserved.

# TODO: sample disclaimer

"Sample pdfprocess client module"


import base64
import json
import sys

import requests


class Client(object):
    BASE_URL = 'https://api.pdfprocess.datalogics-cloud.com'
    VERSION = 0

    ## Set #api_key and #base_url
    #  @param api_key from [3scale](http://datalogics-cloud.3scale.net/)
    def __init__(self, api_key, version=VERSION, base_url=BASE_URL):
        self._api_key = api_key
        self._base_url = '%s/%s' % (base_url, version)

    ## Request factory
    # @return a Request object
    # @param request_type e.g. 'image'
    def make_request(self, request_type):
        if request_type == 'image':
            return ImageRequest(self)

    @property
    ## API key property (string)
    def api_key(self): return self._api_key
    @property
    ## %Client URL property (string)
    def base_url(self): return self._base_url


class Request(object):
    def __init__(self, client, request_type):
        self._url = '%s/actions/%s' % (client.base_url, request_type)
        self._client_data = {'apiKey': client.api_key}
        self.reset()

    ## Post request
    #  @return a requests.Response object
    #  @param input request document file object
    #  @param options e.g. {'pages': '1', 'printPreview': True}
    def post(self, input, **options):
        if input.name: self.data['inputName'] = input.name
        if options: self.data['options'] = json.dumps(options)
        return requests.post(self.url, data=self.data, files={'input': input})

    ## Reset #data
    def reset(self):
        self._data = self._client_data.copy()

    @property
    ## %Request data property (dict), set by #post
    def data(self): return self._data
    @property
    ## %Request URL property (string)
    def url(self): return self._url


class ImageRequest(Request):
    def __init__(self, client):
        Request.__init__(self, client, 'image')

    ## Post request
    #  @return an ImageResponse object
    #  @param input request document file object
    #  @param output_form output graphic format, e.g. 'jpg'
    #  @param options e.g. {'pages': '1', 'printPreview': True}
    #
    #  TODO: add flag descriptions
    #  Set any of the following bool options as needed:
    #  * OPP
    #  * drawAnnotations
    #  * enhanceThinLines
    #  * printPreview
    #  * useCMMWorkflow
    #
    #  TODO: add option descriptions
    #  * colorModel
    #  * compression
    #  * height
    #  * pages
    #  * password
    #  * pdfRegion
    #  * resolution
    #  * smoothing
    #  * width
    #
    #  Each request is for one image, so multi-page requests are limited
    #  to TIFF images.
    #
    #  Option names are case-insensitive.
    def post(self, input, output_form, **options):
        self.reset()
        self.data['outputForm'] = output_form
        return ImageResponse(Request.post(self, input, **options))


## Returned by Request.post
class Response(object):
    def __init__(self, request_response):
        self._status_code = request_response.status_code
        try: self._json = request_response.json()
        except ValueError: self._json = {}
    def __str__(self):
        return '%s: %s' % (response.process_code, response.output)
    def __bool__(self):
        return self.process_code == 0
    __nonzero__ = __bool__
    def __getitem__(self, key):
        return json.dumps(self._json[key])
    @property
    ## API status code (int)
    #
    #  TODO: describe codes
    def process_code(self):
        if 'processCode' in self._json: return int(self['processCode'])

    @property
    ## Base64-encoded data (string) if request was successful, otherwise None
    def output(self):
        if 'output' in self._json and self: return self['output']

    @property
    ## None if successful, otherwise information (string) about #process_code
    def exc_info(self):
        if 'output' in self._json and not self: return self['output']

    @property
    ## HTTP status code (int)
    def status_code(self): return self._status_code


## Returned by ImageRequest.post
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

