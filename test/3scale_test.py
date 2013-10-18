"server regression tests, 3scale"

import uuid
import test

from test_client import StatusCode
from web_api.client import Client
from web_api.errors import Error, ProcessCode
from nose.tools import assert_equal, assert_is_none


def test_auth_ok():
    client = web_api_client(test.TEST_ID, test.TEST_KEY)
    client.authorize()

def test_no_application_id():
    authorize_error(web_api_client(''), 'App Id not defined')

def test_bad_application_id():
    application_id = str(uuid.uuid4())[:8]
    error = 'application with id="{}" was not found'.format(application_id)
    authorize_error(web_api_client(application_id), error)

def test_no_application_key():
    authorize_error(web_api_client(app_key=''), 'application key is missing')

def test_bad_application_key():
    error = 'application key "{}" is invalid'.format(test.PUBLIC_KEY)
    authorize_error(web_api_client(test.TEST_ID), error)

def test_usage_limit_exceeded():
    message = 'usage limits are exceeded'
    for j in range(100):
        try:
            web_api_client().authorize()
        except Error as error:
            process_code = ProcessCode.UsageLimitExceeded
            status_code = StatusCode.TooManyRequests
            validate_error(error, process_code, status_code, message)
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
        process_code = ProcessCode.AuthorizationError
        validate_error(error, process_code, StatusCode.Forbidden, message)

def validate_error(error, process_code, status_code, message):
    assert_equal(process_code, error.process_code)
    assert_equal(status_code, error.status_code)
    assert_equal(message, str(error))
