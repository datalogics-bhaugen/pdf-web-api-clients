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
def render_pages():
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


import random

IM_A_TEAPOT = '''<head><title>I'm a teapot</title></head>
<body>
    <a href="http://joereddington.com/418-error-code-teapot/">
        <img src="{0}" alt="{0}" title="{0}">
    </a>
    <p>Inspired by Joe Reddington and Laurence O'Toole.&nbsp;
        <a href="http://creativecommons.org/licenses/by/3.0/">
            <img src="http://i.creativecommons.org/l/by/3.0/88x31.png"
                 alt="Creative Commons Attribution 3.0 Unported License"
                 title="Creative Commons Attribution 3.0 Unported License">
        </a>
    </p>
</body>
'''

@app.route('/api/actions/brew/coffee', methods=['GET', 'POST'])
def brew_coffee():
    csr_base_url = 'http://www.joereddington.com/csr'
    uploads_base_url = 'http://joereddington.com/wp-content/uploads/2013/09'
    images = ('{}/pot.png'.format(uploads_base_url),
              '{}/withtea.png'.format(csr_base_url),
              '{}/pouring.png'.format(uploads_base_url),
              '{}/shelf.png'.format(csr_base_url))
    return IM_A_TEAPOT.format(images[random.randrange(0, len(images))]), 418
