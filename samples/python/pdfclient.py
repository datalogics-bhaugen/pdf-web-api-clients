# Copyright (c) 2013, Datalogics, Inc. All rights reserved.

# TODO: sample disclaimer

"Sample pdfprocess client module"


import requests


class Client(object):
    BASE_URL = 'https://api.pdfprocess.datalogics-cloud.com'
    VERSION = 0

    ## Set #api_key and #base_url
    #  @param api_key from <a href="http://3scale.net/">TODO: fix link</a>
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
    #  @return a requests.Response object
    #  @param input request document file object
    #  @param output_form output graphic format, e.g. 'JPG'
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
    #  %ImageRequest's 'height' and 'width' options specify the image's
    #  dimensions, replacing [PDF2IMG](../PDF2IMG.pdf)'s pixelcount option.
    #
    #  See PDF2IMG for more information about the remaining options:
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
    def post(self, input, output_form, **options):
        self._data['outputForm'] = output_form
        return Request.post(self, input, **options)

