"server regression tests, JSON"

from pdfprocess.action import Action
from pdfprocess.client import Client
from pdfprocess.errors import Error
from test import MockLogger, TEST_ID, TEST_KEY
from nose.tools import assert_in, assert_raises


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
    assert_raises(Error, Client, logger, {'application': str(application)})
    assert_in(('error', 'cannot parse %s' % application), logger.log)

def test_bad_options():
    logger = MockLogger()
    options = {'outputForm': 'jpg', 'printPreview': True}
    assert_raises(Error, Action, logger, MockRequest(str(options)))
    assert_in(('error', 'cannot parse %s' % options), logger.log)

