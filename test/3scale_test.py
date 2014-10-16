"server regression tests, 3scale"

import json
import uuid
import test

from test import THREE_SCALE
from test_client import HTTPCode
from server.client import Client
from server.errors import Error, ErrorCode, USAGE_LIMIT_ERROR
from nose.tools import assert_equal, assert_is_none


def test_authenticate_ok():
    client(THREE_SCALE.test_id, THREE_SCALE.test_key).authenticate()

def test_jquery_syntax():
    id, key = THREE_SCALE.test_id, THREE_SCALE.test_key
    request_form = {'application[id]': id, 'application[key]': key}
    Client('127.0.0.1', request_form).authenticate()

def test_no_application_id():
    authenticate_error(client(''), 'AuthorizationError: App Id not defined')

def test_bad_application_id():
    id = str(uuid.uuid4())[:8]
    error =\
        'AuthorizationError: application with id="{}" was not found'.format(id)
    authenticate_error(client(id), error)

def test_no_application_key():
    error = 'AuthorizationError: application key is missing'
    authenticate_error(client(key=''), error)

def test_bad_application_key():
    key = THREE_SCALE.public_key
    error = 'AuthorizationError: application key "{}" is invalid'.format(key)
    authenticate_error(client(THREE_SCALE.test_id), error)

def test_usage_limit_exceeded():
    message = 'UsageLimitExceeded: ' + USAGE_LIMIT_ERROR.message
    for j in range(100):
        try:
            client().authenticate()
        except Error as error:
            error_code = ErrorCode.UsageLimitExceeded
            http_code = HTTPCode.TooManyRequests
            validate_error(error, error_code, http_code, message)
            return
    assert_is_none(message)


def authenticate_error(client, message):
    try:
        client.authenticate()
        assert_is_none(message)
    except Error as error:
        error_code = ErrorCode.AuthorizationError
        validate_error(error, error_code, HTTPCode.Forbidden, message)

def client(id=THREE_SCALE.public_id, key=THREE_SCALE.public_key):
    application = json.dumps({'id': id, 'key': key})
    return Client('127.0.0.1', {'application': application})

def validate_error(error, error_code, http_code, message):
    assert_equal(error_code, error.code)
    assert_equal(http_code, error.http_code)
    assert_equal(message, str(error))
