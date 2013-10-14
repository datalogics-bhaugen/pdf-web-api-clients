"server regression tests, 3scale"

import uuid
import mock
import test

from pdfprocess.errors import Auth
from pdfprocess.client import Client
from test import PUBLIC_ID, PUBLIC_KEY
from nose.tools import assert_equal, assert_in, assert_is_none


def test_auth_ok():
    client = pdfprocess_client(test.TEST_ID, test.TEST_KEY)
    assert_equal(client.auth(), Auth.OK)

def test_no_application_id():
    auth_invalid(pdfprocess_client(''), 'App Id not defined')

def test_bad_application_id():
    application_id = str(uuid.uuid4())[:8]
    error = 'application with id="%s" was not found' % application_id
    auth_invalid(pdfprocess_client(application_id), error)

def test_no_application_key():
    auth_invalid(pdfprocess_client(app_key=''), 'application key is missing')

def test_bad_application_key():
    error = 'application key "%s" is invalid' % PUBLIC_KEY
    auth_invalid(pdfprocess_client(test.TEST_ID), error)

def test_usage_limit_exceeded():
    client = pdfprocess_client()
    for j in range(100):
        auth = client.auth()
        if auth == Auth.UsageLimitExceeded: return
        assert_equal(auth, Auth.OK)
    assert_is_none('usage limit exceeded')


def pdfprocess_client(app_id=PUBLIC_ID, app_key=PUBLIC_KEY):
    application = {'id': app_id, 'key': app_key}
    return Client(mock.Logger(), '127.0.0.1', {'application': application})

def auth_invalid(client, error):
    assert_equal(client.auth(), Auth.Invalid)
    if error not in client.exc_info: print(client.exc_info)
    assert_in(error, client.exc_info)
