"thumbnail application"

import flask
import requests
import sys
import traceback

import input
import logger

from StringIO import StringIO
from pdfclient import Application
from cfg import Configuration
from errors import Error, ErrorCode, HTTPCode, UNKNOWN
from request import JSON


BASE_URL = 'http://127.0.0.1:{}'.format(Configuration.service.port)

IMAGE_HEIGHT = 'imageHeight'
IMAGE_WIDTH = 'imageWidth'
INPUT_URL = 'inputURL'
OPTIONS = 'options'
PAGES = 'pages'

MAX_RETRY_ERROR = Error(ErrorCode.UnknownError, 'Max retries exceeded',
                        HTTPCode.TooManyRequests)

three_scale = Configuration.three_scale
api_client = Application(three_scale.thumbnail_id, three_scale.thumbnail_key)

class Action(object):
    "thumbnail request handler"
    def __init__(self, request):
        self._request_time = logger.iso8601_timestamp()
        self._request = request
        self._options = self._request_options()
        self._status_code = HTTPCode.OK
        self._url =\
            request.form.get(INPUT_URL, None) or request.args.get(INPUT_URL)
    def __call__(self):
        url, options = self._url, self._options
        request = api_client.make_request('RenderPages', BASE_URL)
        if IMAGE_WIDTH in self._options or IMAGE_HEIGHT in self._options:
            api_response = request(files={}, inputURL=url, options=options)
            return self._response(api_response)
        return self._smaller_thumbnail(request, url, options)
    def log_usage(self, error=None):
        usage = {'action': 'Thumbnail', 'address': self._request.remote_addr}
        if error:
            Action.log_error(error)
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
        options[IMAGE_WIDTH] = options[IMAGE_HEIGHT]
        del options[IMAGE_HEIGHT]
        landscape_response = api_request(files, options=options)
        if not landscape_response.ok: return self._response(portrait_response)
        if not portrait_response.ok: return self._response(landscape_response)
        return self._response(
            self._smaller_response(portrait_response, landscape_response))
    @classmethod
    def log_error(cls, error):
        logger.error(error)
        if error.code == ErrorCode.UnknownError:
            dlenv = Configuration.environment.dlenv
            for entry in traceback.format_tb(sys.exc_info()[2]):
                logger.error(entry.rstrip())
                if dlenv == 'prod' and '/eggs/' in entry: return

class InputFile(StringIO):
    "file-like class downloads files without using the file system"
    def __init__(self, url):
        StringIO.__init__(self)
        self._url = url
        input.ChunkedTransfer(url, self)
    @property
    def name(self): return self._url

app = flask.Flask(__name__)
logger.start(app.logger, app.name)

@app.route('/', methods=['GET'])
def action():
    action = Action(flask.request)
    try:
        response = action()
        action.log_usage()
        return response
    except Error as error:
        return error_response(action, error)
    except requests.packages.urllib3.exceptions.MaxRetryError:
        return error_response(action, MAX_RETRY_ERROR)
    except Exception as exception:
        return error_response(action, UNKNOWN.copy(str(exception)))
    finally:
        del action

def error_response(action, error):
    "Return the Flask response for an error."
    json = flask.jsonify(errorCode=int(error.code), errorMessage=error.message)
    action.log_usage(error)
    return json, error.http_code
