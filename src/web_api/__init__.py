"web_api application"

import os
import sys
import logging
import traceback

import flask
import logger
import tmpdir

from action import Action
from configuration import Configuration
from errors import EnumValue, Error, ProcessCode, StatusCode, UNKNOWN
from tmpdir import RESOURCE, Stdout, TemporaryFile

import pdf2img


app = flask.Flask(__name__)
configuration = Configuration()
logger.start(app.logger, app.name, configuration.server_version)
logger.info('pdf2img: %s' % configuration.pdf2img_version)

@app.route('/api/actions/render/pages', methods=['POST'])
def pdf2img_action():
    try:
        return pdf2img.Action.from_request(flask.request)()
    except Error as error:
        return error_response(error)
    except Exception as exception:
        return error_response(UNKNOWN.copy(str(exception)))

def error_response(error):
    logger.error(error)
    if error.process_code == ProcessCode.UnknownError: log_traceback()
    return response(error.process_code, error.message, error.status_code)

def log_traceback():
    for entry in traceback.format_tb(sys.exc_info()[2]):
        logger.error(entry.rstrip())
        if '/eggs/' in entry: return

def response(process_code, output, status_code=StatusCode.OK):
    json = flask.jsonify(processCode=int(process_code), output=output)
    return json, status_code
