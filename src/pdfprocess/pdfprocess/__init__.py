"pdfprocess application"

import logging

import flask

from .action import Action
from .errors import Auth, EnumValue, Error, ProcessCode, StatusCode, UNKNOWN
from .handlers import FileHandler, SysLogHandler
from .stdout import Stdout

import image


app = flask.Flask(__name__)

@app.before_first_request
def initialize():
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(SysLogHandler())
    app.logger.addHandler(FileHandler(app.name))
    app.logger.info('%s started' % app.name)

@app.route('/api')
def hello():
    return 'Adobe eBook and PDF technologies for developers!'

@app.route('/api/0/actions/image', methods=['POST'])
def image_action():
    try:
        return image.Action(app.logger, flask.request)()
    except Error as error:
        return _error(error.process_code, error.message, error.status_code)
    except Exception as exception:
        return _error(ProcessCode.UnknownError, exception.message)

def _error(process_code, output, status_code=StatusCode.InternalServerError):
    json = flask.jsonify(processCode=int(process_code), output=output)
    return json, status_code

