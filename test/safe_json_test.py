"server regression tests, safe_json"

from pdfprocess.action import Action
from pdfprocess.client import Client
from test import Logger, PUBLIC_ID, PUBLIC_KEY
from nose.tools import assert_equal, assert_false, assert_in, assert_is_none


class Request(object):
    def __init__(self, options):
        self._options = options
    @property
    def files(self): return {}
    @property
    def form(self): return {'options': self._options}


def test_bad_application():
    logger = Logger()
    application = {'id': PUBLIC_ID, 'key': PUBLIC_KEY}
    client = Client(logger, {'application': str(application)})
    assert_in('[ERROR] cannot parse %s' % application, logger.log)
    assert_false(client.app_id)
    assert_false(client.app_key)

def test_bad_options():
    logger = Logger()
    options = {'outputForm': 'jpg', 'printPreview': True}
    request = Request(str(options))
    action = Action(logger, request)
    assert_in('[ERROR] cannot parse %s' % options, logger.log)
    assert_false(action.client.app_id)
    assert_false(action.client.app_key)
    assert_is_none(action.input)
    assert_equal(action.logger, logger)
    assert_is_none(action.options)
    assert_equal(action.request_form, request.form)

