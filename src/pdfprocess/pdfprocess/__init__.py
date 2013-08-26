"pdfprocess application"

import logging

import flask

from .action import Action
from .errors import Auth, EnumValue, Error, ProcessCode, StatusCode, UNKNOWN
from .file_handler import FileHandler
from .stdout import Stdout

import image


app = flask.Flask(__name__)

@app.before_first_request
def initialize():
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(FileHandler(app.name))
    app.logger.info('%s started' % app.name)

@app.route('/api')
def hello():
    return 'Adobe eBook and PDF technologies for developers!'

@app.route('/api/0/actions/image', methods=['POST'])
def image_action():
    return image.Action(app.logger, flask.request)()

