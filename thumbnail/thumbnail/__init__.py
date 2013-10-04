"thumbnail application"

import flask
import requests

from pdfclient import Application, ImageRequest
from errors import JSON, StatusCode


# BASE_URL = 'http://pdfprocess-test.datalogics-cloud.com'
BASE_URL = 'http://127.0.0.1:5000'
VERSION = Application.VERSION

JOEL_GERACI_ID = 'b0ecd1e6'
JOEL_GERACI_KEY = '5024e1e9c089abd46b419cc17222b86b'

MAX_THUMBNAIL_DIMENSION = 150

class Option(object):
    def __init__(self, name): self._name = name
    def __str__(self): return self._name
    def __eq__(self, other): return str(self).lower() == other.lower()
    def __ne__(self, other): return not self == other

IMAGE_WIDTH = Option('imageWidth')
IMAGE_HEIGHT = Option('imageHeight')
OUTPUT_FORM = Option('outputForm')

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def action():
    try:
        application = Application(JOEL_GERACI_ID, JOEL_GERACI_KEY)
        request = ImageRequest(application, VERSION, BASE_URL)
        input_url = flask.request.form.get('inputURL')
        options = thumbnail_options(flask.request.form)
        if IMAGE_WIDTH in options or IMAGE_HEIGHT in options:
            return response(request.get(input_url, options))
        return smaller_thumbnail(request, input_url, options)
    except Exception as exception:
        return str(exception), StatusCode.UnknownServerError

def thumbnail_options(request_form):
    result = JSON.parse(request_form.get('options', '{}'))
    if OUTPUT_FORM not in result.keys(): result[str(OUTPUT_FORM)] = 'png'
    return result

def smaller_thumbnail(request, input_url, options):
    portrait_options, landscape_options = (options, options.copy())
    portrait_options[str(IMAGE_HEIGHT)] = MAX_THUMBNAIL_DIMENSION
    landscape_options[str(IMAGE_WIDTH)] = MAX_THUMBNAIL_DIMENSION
    portrait_response = request.get(input_url, portrait_options)
    landscape_response = request.get(input_url, landscape_options)
    if landscape_response.process_code: return response(portrait_response)
    if portrait_response.process_code: return response(landscape_response)
    return response(smaller_response(portrait_response, landscape_response))

def smaller_response(response1, response2):
    output1, output2 = (response1.output, response2.output)
    return response2 if len(output2) < len(output1) else response1

def response(request_response):
    return request_response.json(), request_response.status_code
