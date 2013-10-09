"server regression tests, JSON"

import mock
from pdfprocess.action import Action
from pdfprocess.client import Client
from pdfprocess.errors import Error
from test import TEST_ID, TEST_KEY
from nose.tools import assert_equal, assert_in, assert_is_none


def test_bad_application():
    logger = mock.Logger()
    application = {'id': TEST_ID, 'key': TEST_KEY}
    error_message = 'cannot parse %s' % application
    request_form = {'application': str(application)}
    try: assert_is_none(Client(logger, '127.0.0.1', request_form))
    except Error as error: assert_equal(error.message, error_message)

def test_bad_options():
    logger = mock.Logger()
    options = {'outputForm': 'jpg', 'printPreview': True}
    error_message = 'cannot parse %s' % options
    try: assert_is_none(Action(logger, mock.Request(str(options))))
    except Error as error: assert_equal(error.message, error_message)
