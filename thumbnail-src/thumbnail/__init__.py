"thumbnail application"

import flask
import requests

import logger
import tmpdir
from cfg import Configuration
from errors import HTTPCode, JSON
from pdfclient import Application


BASE_URL = 'http://127.0.0.1:5000'

INPUT_NAME = 'inputURL'
MAX_THUMBNAIL_DIMENSION = 150

class Option(object):
    def __init__(self, name): self._name = name
    def __str__(self): return self._name
    def __eq__(self, other): return str(self).lower() == other.lower()
    def __ne__(self, other): return not self == other

IMAGE_WIDTH = Option('imageWidth')
IMAGE_HEIGHT = Option('imageHeight')
OUTPUT_FORM = Option('outputForm')
PAGES = Option('pages')

app = flask.Flask(__name__)
logger.start(app.logger, app.name)

@app.route('/', methods=['GET'])
def action():
    try:
        input_url, options = request_data(flask.request)
        application_id = Configuration.three_scale.thumbnail_id
        application_key = Configuration.three_scale.thumbnail_key
        application = Application(application_id, application_key)
        request = application.make_request('render/pages', BASE_URL)
        for option, value in options.iteritems():
            request.options[option] = value
        if IMAGE_WIDTH in options.keys() or IMAGE_HEIGHT in options.keys():
            return response(request(input_url))
        with tmpdir.TemporaryFile() as input_file:
            input_file.write(requests.get(input_url).content)
            return smaller_thumbnail(request, input_file, options)
    except Exception as exception:
        error = str(exception)
        app.logger.exception(error)
        return error, HTTPCode.InternalServerError

def request_data(request):
    form = request.form
    input_url = form.get(INPUT_NAME, None) or request.args.get(INPUT_NAME)
    result = (input_url, JSON.parse(form.get('options', '{}')))
    app.logger.info('{}: options = {}'.format(*result))
    return result

def smaller_thumbnail(request, input_file, options):
    portrait_options, landscape_options = options, options.copy()
    portrait_options[str(IMAGE_HEIGHT)] = MAX_THUMBNAIL_DIMENSION
    landscape_options[str(IMAGE_WIDTH)] = MAX_THUMBNAIL_DIMENSION
    portrait_response = request(input_file, options=portrait_options)
    landscape_response = request(input_file, options=landscape_options)
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
