# Copyright (c) 2013, Datalogics, Inc. All rights reserved.

'Sample pdfprocess client module'


import requests


class Request(object):
    VERSION = 0
    URL = 'https://api.pdfprocess.datalogics-cloud.com'
    ## @brief set #api_key and #url
    ## @param request_type e.g. 'image'
    ## @param api_key from <a href="http://3scale.net/">TODO: fix link</a>
    def __init__(self, request_type, api_key, version=VERSION, base_url=URL):
        self._api_key = api_key
        self._data = None
        self._url = '%s/%s/actions/%s' % (base_url, version, request_type)

    ## @brief set #data and return a requests.Response object
    ## @param input request document file object
    ## @param options request options, e.g. {'pages': '1', 'noAnnot': True}
    def post(self, input, **options):
        self._data = options.copy()
        self._data['apiKey'] = self.api_key
        self._data['inputFile'] = input.name
        return requests.post(self.url, data=self.data, files={'input': input})

    @property
    ## API key property
    def api_key(self): return self._api_key
    @property
    ## request data property, set by #post
    def data(self): return self._data
    @property
    ## request URL property
    def url(self): return self._url


class ImageRequest(Request):
    ## @param api_key from <a href="http://3scale.net/">TODO: fix link</a>
    def __init__(self, api_key, version=Request.VERSION, base_url=Request.URL):
        request_type = 'image'
        Request.__init__(self, request_type, api_key, version, base_url)

