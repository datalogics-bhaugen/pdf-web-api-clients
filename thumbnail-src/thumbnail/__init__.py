"thumbnail application"

import flask
import requests

import logger

from StringIO import StringIO
from cfg import Configuration
from errors import HTTPCode, JSON
from pdfclient import Application


BASE_URL = 'http://127.0.0.1:5000'

INPUT_URL = 'inputURL'

class InputFile(StringIO):
    def __init__(self, input):
        # TODO: chunked transfer
        StringIO.__init__(self, requests.get(input).content)
        self._input = input
    @property
    def name(self):
        return self._input

class Option(object):
    def __init__(self, name): self._name = name
    def __str__(self): return self._name
    def __eq__(self, other): return str(self).lower() == other.lower()
    def __ne__(self, other): return not self == other

IMAGE_WIDTH = Option('imageWidth')
IMAGE_HEIGHT = Option('imageHeight')
OPTIONS = Option('options')
PAGES = Option('pages')

three_scale = Configuration.three_scale
api_client = Application(three_scale.thumbnail_id, three_scale.thumbnail_key)

app = flask.Flask(__name__)
logger.start(app.logger, app.name)

@app.route('/', methods=['GET'])
def action():
    try:
        options = request_options(flask.request)
        files, input = {}, input_url(flask.request)
        app.logger.info('{}: options = {}'.format(input, options))
        request = api_client.make_request('RenderPages', BASE_URL)
        if str(IMAGE_WIDTH) in options or str(IMAGE_HEIGHT) in options:
            return response(request(files, inputURL=input, options=options))
        return smaller_thumbnail(request, InputFile(input), options)
    except Exception as exception:
        error = str(exception)
        app.logger.exception(error)
        return error, HTTPCode.InternalServerError

def input_url(request):
    key = str(INPUT_URL)
    return request.form.get(key, None) or request.args.get(key)

def request_options(request):
    result = {}
    pages = request.args.get(str(PAGES), None)
    if pages: result[str(PAGES)] = str(pages)
    image_width = request.args.get(str(IMAGE_WIDTH), None)
    if image_width: result[str(IMAGE_WIDTH)] = image_width
    image_height = request.args.get(str(IMAGE_HEIGHT), None)
    if image_height: result[str(IMAGE_HEIGHT)] = image_height
    result.update(JSON.loads(request.form.get(str(OPTIONS), '{}')))
    return result

def smaller_thumbnail(request, input_file, options):
    files, limits = {'input': input_file}, Configuration.limits
    options[str(IMAGE_HEIGHT)] = limits['max_thumbnail_dimension']
    portrait_response = request(files, options=options)
    del options[str(IMAGE_HEIGHT)]
    options[str(IMAGE_WIDTH)] = limits['max_thumbnail_dimension']
    landscape_response = request(files, options=options)
    if not landscape_response: return response(portrait_response)
    if not portrait_response: return response(landscape_response)
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
