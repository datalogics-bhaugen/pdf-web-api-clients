"server regression tests, 3scale"

import uuid
import test

from web_api import Auth
from web_api.client import Client
from nose.tools import assert_equal, assert_is_none


def test_auth_ok():
    client = web_api_client(test.TEST_ID, test.TEST_KEY)
    assert_equal(client.auth(), Auth.OK)

def test_no_application_id():
    auth_invalid(web_api_client(''), 'App Id not defined')

def test_bad_application_id():
    application_id = str(uuid.uuid4())[:8]
    error = 'application with id="%s" was not found' % application_id
    auth_invalid(web_api_client(application_id), error)

def test_no_application_key():
    auth_invalid(web_api_client(app_key=''), 'application key is missing')

def test_bad_application_key():
    error = 'application key "%s" is invalid' % test.PUBLIC_KEY
    auth_invalid(web_api_client(test.TEST_ID), error)

def test_usage_limit_exceeded():
    client = web_api_client()
    error = 'usage limits are exceeded'
    for j in range(100):
        auth = client.auth()
        if auth == Auth.UsageLimitExceeded:
            assert_equal(error, client.exc_info)
            return
        assert_equal(auth, Auth.OK)
    assert_is_none(error)


def web_api_client(app_id=test.PUBLIC_ID, app_key=test.PUBLIC_KEY):
    application = {'id': app_id, 'key': app_key}
    return Client('127.0.0.1', {'application': application})

def auth_invalid(client, error):
    assert_equal(client.auth(), Auth.Invalid)
    if error not in client.exc_info: print(client.exc_info)
    assert_equal(error, client.exc_info)
