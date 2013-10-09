"server regression tests, 3scale"

import uuid
import mock
import test

from pdfprocess.errors import Auth
from pdfprocess.client import Client
from test import PUBLIC_ID, PUBLIC_KEY
from nose.tools import assert_equal, assert_is_none


def pdfprocess_client(app_id=PUBLIC_ID, app_key=PUBLIC_KEY):
    application = {'id': app_id, 'key': app_key}
    return Client(mock.Logger(), '127.0.0.1', {'application': application})


def test_auth_ok():
    client = pdfprocess_client(test.TEST_ID, test.TEST_KEY)
    assert_equal(client.auth(), Auth.OK)

def test_no_application_id():
    client = pdfprocess_client('')
    assert_equal(client.auth(), Auth.Invalid)

def test_bad_application_id():
    client = pdfprocess_client(str(uuid.uuid4())[:8])
    assert_equal(client.auth(), Auth.Invalid)

def test_no_application_key():
    client = pdfprocess_client(app_key='')
    assert_equal(client.auth(), Auth.Invalid)

def test_bad_application_key():
    client = pdfprocess_client(test.TEST_ID)
    assert_equal(client.auth(), Auth.Invalid)

def test_usage_limit_exceeded():
    client = pdfprocess_client()
    for j in range(100):
        auth = client.auth()
        if auth == Auth.UsageLimitExceeded: return
        assert_equal(auth, Auth.OK)
    assert_is_none('usage limit exceeded')
