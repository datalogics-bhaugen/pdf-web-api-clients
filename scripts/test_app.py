"pdfprocess regression tests"

import flask
import pdfprocess
from flask.testing import FlaskClient
from nose.tools import assert_equal, assert_in

NOT_FOUND = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>
'''

class TestNotFound(object):
    def abort(self):
        flask.abort(404)

    def setup(self):
        pdfprocess.app.add_url_rule('/404', 'NOT FOUND', self.abort)
        self._app = FlaskClient(pdfprocess.app)

    def test_default_error_result(self):
        data, status, headers = self._app.get('/404')
        assert_equal(status, '404 NOT FOUND')
        assert_equal(headers['Content-Type'], 'text/html')
        assert_equal(next(data), NOT_FOUND)

