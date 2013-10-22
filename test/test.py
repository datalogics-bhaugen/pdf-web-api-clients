"server test classes"

import test_client
from test_client import HTTPCode, THREE_SCALE
from nose.tools import assert_equal, assert_in
from nose.tools import assert_is_none, assert_is_not_none


BASE_URL = 'http://127.0.0.1:5000'


class Result(object):
    def __init__(self, error_code=None, http_code=HTTPCode.OK):
        if error_code and http_code == HTTPCode.OK:
            http_code = HTTPCode.BadRequest
        self._error_code, self._http_code = error_code, http_code
    def validate(self, response):
        assert_equal(self._error_code, response.error_code)
        if isinstance(self._http_code, int):
            assert_equal(response.http_code, self._http_code)
        else:
            assert_in(response.http_code, self._http_code)
        if response:
            assert_is_not_none(response.output)
            assert_is_none(response.error_message)
        else:
            assert_is_none(response.output)
            assert_is_not_none(response.error_message)
        return response

class Test(object):
    def __init__(self, args, result, client=None):
        self._args, self._result = args, result
        self._client = client or Test.client()
    def __call__(self, base_url=BASE_URL):
        return self._result.validate(self.post(base_url))
    def post(self, base_url):
        return self._client(['test', 'render/pages'] + self._args, base_url)
    @classmethod
    def client(cls, id=THREE_SCALE.test_id, key=THREE_SCALE.test_key):
        return test_client.client(id, key)
