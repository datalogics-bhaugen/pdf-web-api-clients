"server regression tests, 3scale"

import uuid
import test

from test_client import HTTPCode
from web_api.client import Client
from web_api.errors import Error, ErrorCode
from nose.tools import assert_equal, assert_is_none


def test_auth_ok():
    client = web_api_client(test.TEST_ID, test.TEST_KEY)
    client.authorize()

def test_no_application_id():
    error = 'AuthorizationError: App Id not defined'
    authorize_error(web_api_client(''), error)

def test_bad_application_id():
    id = str(uuid.uuid4())[:8]
    error =\
        'AuthorizationError: application with id="{}" was not found'.format(id)
    authorize_error(web_api_client(id), error)

def test_no_application_key():
    error = 'AuthorizationError: application key is missing'
    authorize_error(web_api_client(app_key=''), error)

def test_bad_application_key():
    key = test.PUBLIC_KEY
    error = 'AuthorizationError: application key "{}" is invalid'.format(key)
    authorize_error(web_api_client(test.TEST_ID), error)

def test_usage_limit_exceeded():
    message = 'UsageLimitExceeded: usage limits are exceeded'
    for j in range(100):
        try:
            web_api_client().authorize()
        except Error as error:
            error_code = ErrorCode.UsageLimitExceeded
            http_code = HTTPCode.TooManyRequests
            validate_error(error, error_code, http_code, message)
            return
    assert_is_none(message)


def web_api_client(app_id=test.PUBLIC_ID, app_key=test.PUBLIC_KEY):
    application = {'id': app_id, 'key': app_key}
    return Client('127.0.0.1', {'application': application})

def authorize_error(client, message):
    try:
        client.authorize()
        assert_is_none(message)
    except Error as error:
        error_code = ErrorCode.AuthorizationError
        validate_error(error, error_code, HTTPCode.Forbidden, message)

def validate_error(error, error_code, http_code, message):
    assert_equal(error_code, error.code)
    assert_equal(http_code, error.http_code)
    assert_equal(message, str(error))
