"server regression tests, JSON"

import mock
from web_api.action import Action
from web_api.client import Client
from web_api.errors import Error
from test import TEST_ID, TEST_KEY
from nose.tools import assert_equal, assert_in, assert_is_none


def test_bad_application():
    application = {'id': TEST_ID, 'key': TEST_KEY}
    error_message = 'cannot parse {}'.format(application)
    request_form = {'application': str(application)}
    try: assert_is_none(Client('127.0.0.1', request_form))
    except Error as error: assert_equal(error.message, error_message)

def test_bad_options():
    options = {'outputFormat': 'jpg', 'printPreview': True}
    error_message = 'cannot parse {}'.format(options)
    try: assert_is_none(Action(mock.Request(str(options))))
    except Error as error: assert_equal(error.message, error_message)
