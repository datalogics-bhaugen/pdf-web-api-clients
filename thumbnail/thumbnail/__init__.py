"thumbnail application"

import flask
import requests

import logger
import tmpdir
from errors import JSON, StatusCode
from pdfclient import Application


BASE_URL = 'http://127.0.0.1:5000'

JOEL_GERACI_ID = 'b0ecd1e6'
JOEL_GERACI_KEY = '5024e1e9c089abd46b419cc17222b86b'

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
        application = Application(JOEL_GERACI_ID, JOEL_GERACI_KEY)
        request = application.make_request('render/pages', BASE_URL)
        if IMAGE_WIDTH in options.keys() or IMAGE_HEIGHT in options.keys():
            return response(request(input_url, options=options))
        with tmpdir.TemporaryFile() as input_file:
            input_file.write(requests.get(input_url).content)
            return smaller_thumbnail(request, input_file, options)
    except Exception as exception:
        error = str(exception)
        app.logger.exception(error)
        return error, StatusCode.InternalServerError

def request_data(request):
    form = request.form
    input_url = form.get(INPUT_NAME, None) or request.args.get(INPUT_NAME)
    result = (input_url, JSON.parse(form.get('options', '{}')))
    app.logger.info('{}: options = {}'.format(result))
    return result

def smaller_thumbnail(request, input_file, options):
    portrait_options, landscape_options = options, options.copy()
    portrait_options[str(IMAGE_HEIGHT)] = MAX_THUMBNAIL_DIMENSION
    landscape_options[str(IMAGE_WIDTH)] = MAX_THUMBNAIL_DIMENSION
    portrait_response = request(input_file, options=portrait_options)
    landscape_response = request(input_file, options=landscape_options)
    if landscape_response.process_code: return response(portrait_response)
    if portrait_response.process_code: return response(landscape_response)
    return response(smaller_response(portrait_response, landscape_response))

def smaller_response(response1, response2):
    output1, output2 = response1['output'], response2['output']
    return response2 if len(output2) < len(output1) else response1

def response(request_response):
    process_code = int(request_response['processCode'])
    status_code = request_response.status_code
    output = request_response['output']
    return flask.jsonify(processCode=process_code, output=output), status_code
