"server regression tests, 3scale"

import uuid
import test

from pdfprocess.client import Client
from pdfprocess.errors import Auth
from nose.tools import assert_equal, assert_false


RATE_LIMITED_ID = 'c953bc0d'
RATE_LIMITED_KEY = 'c7a7c21fb25c384127879ded5ed3b0a4'


class Logger:
    def error(self, exc):
        print('error: %s' % exc)

def pdfprocess_client(app_id, app_key):
    return Client(Logger(), '{"id": "%s", "key": "%s"}' % (app_id, app_key))


def test_bad_application_id():
    bad_application_id = str(uuid.uuid4())[:8]
    client = pdfprocess_client(bad_application_id, test.APPLICATION_KEY)
    assert_equal(client.auth(), Auth.Invalid)

def test_bad_application_key():
    bad_application_key = str(uuid.uuid4()).replace('-', '')
    client = pdfprocess_client(test.APPLICATION_ID, bad_application_key)
    assert_equal(client.auth(), Auth.Invalid)

def test_usage_limit_exceeded():
    client = pdfprocess_client(RATE_LIMITED_ID, RATE_LIMITED_KEY)
    for j in range(100):
        auth = client.auth()
        if auth == Auth.TooFast: return
        assert_equal(auth, Auth.OK)
    assert_false('usage limit exceeded')

