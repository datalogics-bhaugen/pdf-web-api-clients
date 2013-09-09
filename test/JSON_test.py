"server regression tests, JSON"

from pdfprocess.action import Action
from pdfprocess.client import Client
from pdfprocess.errors import Error
from test import MockLogger, TEST_ID, TEST_KEY
from nose.tools import assert_equal, assert_in, assert_is_none


class MockRequest(object):
    def __init__(self, options):
        self._options = options
    @property
    def files(self): return {}
    @property
    def form(self): return {'options': self._options}


def test_bad_application():
    logger = MockLogger()
    application = {'id': TEST_ID, 'key': TEST_KEY}
    error_message = 'cannot parse %s' % application
    try: assert_is_none(Client(logger, {'application': str(application)}))
    except Error as error: assert_equal(error.message, error_message)
    assert_in(('error', error_message), logger.log)

def test_bad_options():
    logger = MockLogger()
    options = {'outputForm': 'jpg', 'printPreview': True}
    error_message = 'cannot parse %s' % options
    try: assert_is_none(Action(logger, MockRequest(str(options))))
    except Error as error: assert_equal(error.message, error_message)
    assert_in(('error', error_message), logger.log)

