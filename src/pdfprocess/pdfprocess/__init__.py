"pdfprocess application"

import logging

import flask

from .action import Action
from .error import Auth, Error, ImageProcessCode, ProcessCode, StatusCode
from .file_handler import FileHandler
from .stdout import Stdout

import image


app = flask.Flask(__name__)
app.logger.setLevel(logging.DEBUG) # TODO: get level from configuration
app.logger.addHandler(FileHandler(app.name))

@app.before_first_request
def initialize():
    app.logger.info('%s started' % app.name)

@app.route('/api')
def hello():
    return 'Adobe eBook and PDF technologies for developers!'

@app.route('/api/0/actions/image', methods=['POST'])
def image_action():
    return image.Action(app.logger, flask.request)()

