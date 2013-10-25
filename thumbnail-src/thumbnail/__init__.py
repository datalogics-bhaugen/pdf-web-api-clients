"thumbnail application"

import flask
import requests

import logger
import tmpdir
from cfg import Configuration
from errors import HTTPCode, JSON
from pdfclient import Application


BASE_URL = 'http://127.0.0.1:5000'

INPUT_URL = 'inputURL'
MAX_THUMBNAIL_DIMENSION = 250

class Option(object):
    def __init__(self, name): self._name = name
    def __str__(self): return self._name
    def __eq__(self, other): return str(self).lower() == other.lower()
    def __ne__(self, other): return not self == other

IMAGE_WIDTH = Option('imageWidth')
IMAGE_HEIGHT = Option('imageHeight')
OPTIONS = Option('options')
PAGES = Option('pages')

app = flask.Flask(__name__)
logger.start(app.logger, app.name)

@app.route('/', methods=['GET'])
def action():
    try:
        request = application().make_request('render/pages', BASE_URL)
        request.options.update(request_options(flask.request))
        input, options = input_url(flask.request), request.options
        app.logger.info('{}: options = {}'.format(input, options))
        if str(IMAGE_WIDTH) in options or str(IMAGE_HEIGHT) in options:
            return response(request(input))
        with tmpdir.TemporaryFile() as input_file:
            input_file.write(requests.get(input).content)
            return smaller_thumbnail(request, input_file)
    except Exception as exception:
        error = str(exception)
        app.logger.exception(error)
        return error, HTTPCode.InternalServerError

def application():
    three_scale = Configuration.three_scale
    return Application(three_scale.thumbnail_id, three_scale.thumbnail_key)

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
    result.update(JSON.parse(request.form.get(str(OPTIONS), '{}')))
    return result

def smaller_thumbnail(request, input_file):
    request.options[str(IMAGE_HEIGHT)] = MAX_THUMBNAIL_DIMENSION
    portrait_response = request(input_file)
    del request.options[str(IMAGE_HEIGHT)]
    request.options[str(IMAGE_WIDTH)] = MAX_THUMBNAIL_DIMENSION
    landscape_response = request(input_file)
    if landscape_response: return response(portrait_response)
    if portrait_response: return response(landscape_response)
    return response(smaller_response(portrait_response, landscape_response))

def smaller_response(api_response_1, api_response_2):
    output1, output2 = api_response_1.output, api_response_2.output
    return api_response_2 if len(output2) < len(output1) else api_response_1

def response(api_response):
    if api_response:
        return api_response.output
    else:
        code, message = api_response.error_code, api_response.error_message
        json = flask.jsonify(errorCode=code, errorMessage=message)
        return json, api_response.status_code
