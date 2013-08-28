"server regression tests, 3scale"

import uuid
import test

from pdfprocess.errors import Auth
from pdfprocess.client import Client
from nose.tools import assert_equal, assert_false


PUBLIC_ID = 'c953bc0d'
PUBLIC_KEY = 'c7a7c21fb25c384127879ded5ed3b0a4'


class Logger:
    def __getattr__(self, name):
        return self._logger(name)
    def _logger(self, name):
        def log(value): print('%s: %s' % (name, value))
        return log

def pdfprocess_client(app_id=PUBLIC_ID, app_key=PUBLIC_KEY):
    return Client(Logger(), {'application': {'id': app_id, 'key': app_key}})


def test_auth_ok():
    assert_equal(pdfprocess_client().auth(), Auth.OK)

def test_bad_application_id():
    client = pdfprocess_client(str(uuid.uuid4())[:8])
    assert_equal(client.auth(), Auth.Invalid)

def test_bad_application_key():
    client = pdfprocess_client(test.TEST_ID)
    assert_equal(client.auth(), Auth.Invalid)

def test_bad_application_json():
    application_json = {'id': PUBLIC_ID, 'key': PUBLIC_KEY}
    client = Client(Logger(), {'application': str(application_json)})
    assert_false(client.app_id)
    assert_false(client.app_key)

def test_usage_limit_exceeded():
    client = pdfprocess_client()
    for j in range(100):
        auth = client.auth()
        if auth == Auth.TooFast: return
        assert_equal(auth, Auth.OK)
    assert_false('usage limit exceeded')

