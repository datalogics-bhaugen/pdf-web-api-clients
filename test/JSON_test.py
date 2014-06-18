"server regression tests, JSON"

import mock
from server.action import Action
from server.cfg import Configuration
from server.client import Client
from server.errors import Error
from nose.tools import assert_equal, assert_in, assert_is_none


def test_bad_application():
    three_scale = Configuration.three_scale
    application = {'id': three_scale.test_id, 'key': three_scale.test_key}
    error_message = 'cannot parse {}'.format(application)
    request_form = {'application': str(application)}
    try: assert_is_none(Client('127.0.0.1', request_form))
    except Error as error: assert_equal(error.message, error_message)

def test_bad_options():
    class MockAction(Action):
        def __call__(self): pass
        def request_type(self): return None
    options = {'outputFormat': 'jpg', 'printPreview': True}
    error_message = 'cannot parse {}'.format(options)
    try: assert_is_none(MockAction(mock.Request(str(options))))
    except Error as error: assert_equal(error.message, error_message)
