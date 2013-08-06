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
    ## API key property
    def api_key(self): return self._api_key
    @property
    ## %Client URL property
    def base_url(self): return self._base_url


class Request(object):
    def __init__(self, client, request_type):
        self._data = {'apiKey': client.api_key}
        self._url = '%s/actions/%s' % (client.base_url, request_type)

    ## Post request
    #  @return a requests.Response object
    #  @param input request document file object
    #  @param options e.g. {'pages': '1', 'noAnnot': True}
    def post(self, input, **options):
        self._data.update(options)
        self._data['inputFile'] = input.name
        return requests.post(self.url, data=self.data, files={'input': input})

    @property
    ## %Request data property, set by #post
    def data(self): return self._data
    @property
    ## %Request URL property
    def url(self): return self._url


class ImageRequest(Request):
    def __init__(self, client):
        Request.__init__(self, client, 'image')

    ## Post request
    #  @return an ImageResponse object
    #  @param input request document file object
    #  @param output_form output graphic format, e.g. 'jpg'
    #  @param options e.g. {'pages': '1', 'noAnnot': True}
    #
    #  The following options are interpreted as bool (default=False):
    #  * OPP
    #  * asPrinted
    #  * blackIsOne
    #  * noAnnot
    #  * noCMM
    #  * noEnhanceThinLines
    #  * reverse
    #
    #  The 'height' and 'width' options specify the image's dimensions,
    #  replacing PDF2IMG's pixelcount option.
    #
    #  See [PDF2IMG](http://www.datalogics.com/pdf/doc/pdf2img.pdf)
    #  for more information about the remaining options:
    #  * BPC
    #  * colorModel
    #  * compression
    #  * fontList
    #  * jpegQuality
    #  * maxBandMem
    #  * output
    #  * pages
    #  * password
    #  * pdfRegion
    #  * resolution
    #  * smoothing
    #
    #  Multiple pages may be specified only if output_form is 'TIF'.
    #
    #  Option names are case-insensitive.
    def post(self, input, output_form, **options):
        self._data['outputForm'] = output_form
        return ImageResponse(Request.post(self, input, **options))


## Returned by Request.post
class Response(object):
    def __init__(self, request_response):
        self._json = request_response.json()
        self._status_code = request_response.status_code
    def __str__(self):
        return '%s: %s' % (response.process_code, response.output)
    def __bool__(self):
        return not self.process_code
    def __getitem__(self, key):
        return json.dumps(self._json[key])
    @property
    ## API status code
    #
    #  TODO: describe codes
    def process_code(self): return int(self['processCode'])

    @property
    ## None if successful, otherwise information about the request failure
    def exc_info(self): return not self and self['output']
    @property
    ## Base64-encoded data if request was successful, otherwise None
    def output(self): return self and self['output']
    @property
    ## HTTP status code
    def status_code(self): return self._status_code


## Returned by ImageRequest.post
class ImageResponse(Response):
    def __init__(self, request_response):
        Response.__init__(self, request_response)
    def _image(self):
        if sys.version_info.major < 3:
            return self['output'].decode('base64')
        else:
            return base64.b64decode(self['output'])
    @property
    ## Image data (decoded) if request was successful, otherwise None
    def output(self): return self and self._image()

