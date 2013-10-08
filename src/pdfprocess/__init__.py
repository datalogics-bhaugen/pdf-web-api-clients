"pdfprocess application"

import os
import sys
import logging
import traceback

import flask
import handlers
import tmpdir

from action import Action
from errors import Auth, EnumValue, Error, ProcessCode, StatusCode, UNKNOWN
from tmpdir import RESOURCE, Stdout, TemporaryFile, TMPDIR
from version import Version

import image


app = flask.Flask(__name__)
handlers.start(app.logger, app.name)

# TODO: log version info earlier
@app.before_first_request
def initialize():
    data = Version().get_version_data('../apiversion.ini')
    api_version = data.get('webapi-version')
    app.logger.info('WEBAPIVERSION=%s' % api_version)
    pdf2img_version = data.get('pdf2img-version')
    app.logger.info('PDF2IMGVERSION=%s' % pdf2img_version)

@app.route('/api')
def hello():
    return 'Adobe eBook and PDF technologies for developers!'

@app.route('/api/0/actions/image', methods=['POST'])
def image_action():
    try:
        input_url = flask.request.form.get('inputURL', None)
        action = image.FromURL if input_url else image.FromFile
        return action(app.logger, flask.request)()
    except Error as error:
        return error_response(error)
    except Exception as exception:
        return error_response(UNKNOWN.copy(str(exception)))

def error_response(error):
    app.logger.error(error)
    if error.process_code == ProcessCode.UnknownError: log_traceback()
    return response(error.process_code, error.message, error.status_code)

def log_traceback():
    for entry in traceback.format_tb(sys.exc_info()[2]):
        app.logger.error(entry.rstrip())
        if '/eggs/' in entry: return

def response(process_code, output, status_code=StatusCode.OK):
    json = flask.jsonify(processCode=int(process_code), output=output)
    return json, status_code
