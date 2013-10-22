"WebAPI application"

import os
import sys
import logging
import traceback

import flask
import logger
import tmpdir

from action import Action
from cfg import Configuration
from errors import EnumValue, Error, ErrorCode, HTTPCode, UNKNOWN
from tmpdir import RESOURCE, Stdout, TemporaryFile

import pdf2img


app = flask.Flask('pdfprocess')
logger.start(app.logger, app.name, Configuration.versions.server)

@app.route('/api/actions/render/pages', methods=['POST'])
def pdf2img_action():
    try:
        return pdf2img.Action.from_request(flask.request)()
    except Error as error:
        return response(error)
    except Exception as exception:
        return response(UNKNOWN.copy(str(exception)))

def response(error):
    logger.error(error)
    if error.code == ErrorCode.UnknownError: log_traceback()
    json = flask.jsonify(errorCode=int(error.code), errorMessage=error.message)
    return json, error.http_code

def log_traceback():
    for entry in traceback.format_tb(sys.exc_info()[2]):
        logger.error(entry.rstrip())
        if '/eggs/' in entry: return
