"thumbnail application"

import flask
import requests

import input
import logger

from StringIO import StringIO
from cfg import Configuration
from pdfclient import Application
from errors import Error, HTTPCode
from request import JSON


BASE_URL = 'http://127.0.0.1:{}'.format(Configuration.service.port)

IMAGE_HEIGHT = 'imageHeight'
IMAGE_WIDTH = 'imageWidth'
INPUT_URL = 'inputURL'
OPTIONS = 'options'
PAGES = 'pages'

class InputFile(StringIO):
    "file-like class downloads files without using the file system"
    def __init__(self, url):
        StringIO.__init__(self)
        self._url = url
        input.ChunkedTransfer(url, self)
    @property
    def name(self): return self._url

three_scale = Configuration.three_scale
api_client = Application(three_scale.thumbnail_id, three_scale.thumbnail_key)

app = flask.Flask(__name__)
logger.start(app.logger, app.name)

@app.route('/', methods=['GET'])
def action():
    try:
        client_addr = flask.request.remote_addr
        url, options = input_url(flask.request), request_options(flask.request)
        logger.info('{}: options = {} ({})'.format(url, options, client_addr))
        request = api_client.make_request('RenderPages', BASE_URL)
        if IMAGE_WIDTH in options or IMAGE_HEIGHT in options:
            return response(request(files={}, inputURL=url, options=options))
        return smaller_thumbnail(request, url, options)
    except Error as error:
        return error.message, error.http_code
    except Exception as exception:
        error = str(exception)
        logger.error(error)
        return error, HTTPCode.InternalServerError

def input_url(request):
    return request.form.get(INPUT_URL, None) or request.args.get(INPUT_URL)

def request_options(request):
    result = {}
    pages = request.args.get(PAGES, None)
    if pages: result[PAGES] = str(pages)
    image_width = request.args.get(IMAGE_WIDTH, None)
    if image_width: result[IMAGE_WIDTH] = image_width
    image_height = request.args.get(IMAGE_HEIGHT, None)
    if image_height: result[IMAGE_HEIGHT] = image_height
    result.update(JSON.loads(request.form.get(OPTIONS, '{}')))
    return result

def smaller_thumbnail(api_request, url, options):
    files = {'input': InputFile(url)}
    options[IMAGE_HEIGHT] = Configuration.limits['max_thumbnail_dimension']
    portrait_response = api_request(files, options=options)
    options[IMAGE_WIDTH] = options[IMAGE_HEIGHT]
    del options[IMAGE_HEIGHT]
    landscape_response = api_request(files, options=options)
    if not landscape_response.ok: return response(portrait_response)
    if not portrait_response.ok: return response(landscape_response)
    return response(smaller_response(portrait_response, landscape_response))

def smaller_response(response1, response2):
    output1, output2 = response1.output, response2.output
    return response2 if len(output2) < len(output1) else response1

def response(api_response):
    if api_response.ok:
        content_type = api_response.headers['Content-Type']
        return flask.Response(api_response.output, content_type=content_type)
    else:
        code, message = api_response.error_code, api_response.error_message
        json = flask.jsonify(errorCode=code, errorMessage=message)
        return json, api_response.status_code
