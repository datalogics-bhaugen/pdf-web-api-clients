"thumbnail application"

import os
import sys

import flask
import requests

this_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(this_dir)))
sys.path[0:0] = [os.path.join(root_dir, 'samples', 'python')]

from pdfclient import Application, ImageRequest


BASE_URL = 'http://pdfprocess-test.datalogics-cloud.com'
VERSION = Application.VERSION

JOEL_GERACI_ID = 'b0ecd1e6'
JOEL_GERACI_KEY = '5024e1e9c089abd46b419cc17222b86b'

OUTPUT_FORM = 'png'

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def action():
    application = Application(JOEL_GERACI_ID, JOEL_GERACI_KEY)
    request = ImageRequest(application, VERSION, BASE_URL)
    # TODO: landscape_options = {'imageWidth': 150, 'outputForm': OUTPUT_FORM}
    portrait_options = {'imageHeight': 150, 'outputForm': OUTPUT_FORM}
    return request.get(flask.request.form.get('inputURL'), portrait_options)
    # TODO: compare landscape and portrait thumbnails, return the smaller one
