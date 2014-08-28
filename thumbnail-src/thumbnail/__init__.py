"thumbnail application"

import flask
import requests

import logger

from errors import Error, ErrorCode, HTTPCode, UNKNOWN
from request_handler import RequestHandler


MAX_RETRY_ERROR = Error(ErrorCode.UnknownError, 'Max retries exceeded',
                        HTTPCode.TooManyRequests)

app = flask.Flask(__name__)
logger.start(app.logger, app.name)

@app.route('/', methods=['GET'])
def get_thumbnail():
    request_handler = RequestHandler(flask.request)
    try:
        response = request_handler()
        request_handler.log_usage()
        return response
    except Error as error:
        return error_response(request_handler, error)
    except requests.packages.urllib3.exceptions.MaxRetryError:
        return error_response(request_handler, MAX_RETRY_ERROR)
    except Exception as exception:
        return error_response(request_handler, UNKNOWN.copy(str(exception)))
    finally:
        del request_handler

def error_response(request_handler, error):
    "Return the Flask response for an error."
    json = flask.jsonify(errorCode=int(error.code), errorMessage=error.message)
    request_handler.log_usage(error)
    return json, error.http_code
