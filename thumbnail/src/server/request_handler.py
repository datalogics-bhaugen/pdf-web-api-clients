"The thumbnail server downloads request input and passes this to PDF WebAPI."

import flask

import input
import logger
import usage_limit

from StringIO import StringIO
from pdfclient import Application, ErrorCode
from cfg import Configuration
from errors import Error, HTTPCode
from request import JSON


BASE_URL = 'http://127.0.0.1:{}'.format(Configuration.service.port)

INVALID_INPUT = [ErrorCode.InvalidInput, ErrorCode.MissingPassword,
                 ErrorCode.UnsupportedSecurityProtocol, ErrorCode.InvalidPage]

IMAGE_HEIGHT = 'imageHeight'
IMAGE_WIDTH = 'imageWidth'
INPUT_URL = 'inputURL'
OPTIONS = 'options'
PAGES = 'pages'

three_scale = Configuration.three_scale
api_client = Application(three_scale.thumbnail_id, three_scale.thumbnail_key)

class RequestHandler(object):
    "The server creates a request handler to process a thumbnail request."
    def __init__(self, request):
        self._request_time = logger.iso8601_timestamp()
        self._request = request
        self._options = self._request_options()
        self._status_code = HTTPCode.OK
        self._url =\
            request.form.get(INPUT_URL, None) or request.args.get(INPUT_URL)
    def __call__(self):
        usage_limit.validate(self._request)
        url, options = self._url, self._options
        request = api_client.make_request('RenderPages', BASE_URL)
        if IMAGE_WIDTH in self._options or IMAGE_HEIGHT in self._options:
            api_response = request(files={}, inputURL=url, options=options)
            return self._response(api_response)
        return self._smaller_thumbnail(request, url, options)
    def log_usage(self, error=None):
        "Create a log entry for this request."
        usage = {'action': 'Thumbnail', 'address': self._request.remote_addr}
        if error:
            error.log()
            error_code = int(error.code)
            usage['error'] = {'code': error_code, 'message': error.message}
        usage['inputURL'] = self._url
        usage['options'] = self._options
        usage['requestTime'] = self._request_time
        usage['responseTime'] = logger.iso8601_timestamp()
        usage['status'] = error.http_code if error else self._status_code
        usage['serverVersion'] = Configuration.versions.server_tag
        logger.info(JSON.dumps(usage))
    def _request_options(self):
        result = {}
        pages = self._request.args.get(PAGES, None)
        if pages: result[PAGES] = str(pages)
        image_width = self._request.args.get(IMAGE_WIDTH, None)
        if image_width: result[IMAGE_WIDTH] = image_width
        image_height = self._request.args.get(IMAGE_HEIGHT, None)
        if image_height: result[IMAGE_HEIGHT] = image_height
        result.update(JSON.loads(self._request.form.get(OPTIONS, '{}')))
        return result
    def _response(self, api_response):
        if api_response.ok:
            response = api_response.output
            content_type = api_response.headers['Content-Type']
            return flask.Response(response, content_type=content_type)
        else:
            code, message = api_response.error_code, api_response.error_message
            json = flask.jsonify(errorCode=code, errorMessage=message)
            self._status_code = api_response.status_code
            return json, self._status_code
    def _smaller_response(self, response1, response2):
        output1, output2 = response1.output, response2.output
        return response2 if len(output2) < len(output1) else response1
    def _smaller_thumbnail(self, api_request, url, options):
        files = {'input': InputFile(url)}
        options[IMAGE_HEIGHT] = Configuration.limits['max_thumbnail_dimension']
        portrait_response = api_request(files, options=options)
        if portrait_response.error_code in INVALID_INPUT:
            return self._response(portrait_response)
        options[IMAGE_WIDTH] = options[IMAGE_HEIGHT]
        del options[IMAGE_HEIGHT]
        landscape_response = api_request(files, options=options)
        if not landscape_response.ok: return self._response(portrait_response)
        if not portrait_response.ok: return self._response(landscape_response)
        return self._response(
            self._smaller_response(portrait_response, landscape_response))

class InputFile(StringIO):
    "This file-like class downloads files without using the file system."
    def __init__(self, url):
        StringIO.__init__(self)
        self._url = url
        input.ChunkedTransfer(url, self)
    @property
    def name(self):
        "The input URL."
        return self._url
