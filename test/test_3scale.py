"server regression tests, 3scale"

import uuid
import test

from pdfprocess.client import Client
from pdfprocess.errors import Auth
from nose.tools import assert_equal, assert_false


PUBLIC_ID = 'c953bc0d'
PUBLIC_KEY = 'c7a7c21fb25c384127879ded5ed3b0a4'


class Logger:
    def error(self, exc):
        print('error: %s' % exc)

def pdfprocess_client(app_id, app_key):
    return Client(Logger(), '{"id": "%s", "key": "%s"}' % (app_id, app_key))


def test_bad_application_id():
    client = pdfprocess_client(str(uuid.uuid4())[:8], test.TEST_KEY)
    assert_equal(client.auth(), Auth.Invalid)

def test_bad_application_key():
    client = pdfprocess_client(test.TEST_ID, PUBLIC_KEY)
    assert_equal(client.auth(), Auth.Invalid)

def _test_usage_limit_exceeded():
    client = pdfprocess_client(PUBLIC_ID, PUBLIC_KEY)
    for j in range(100):
        auth = client.auth()
        if auth == Auth.TooFast: return
        assert_equal(auth, Auth.OK)
    assert_false('usage limit exceeded')

