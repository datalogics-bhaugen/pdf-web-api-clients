"server test classes"

import test_client
from test_client import StatusCode
from nose.tools import assert_equal, assert_in
from nose.tools import assert_is_none, assert_is_not_none


BASE_URL = 'http://127.0.0.1:5000'

PUBLIC_ID = 'c953bc0d'
PUBLIC_KEY = 'c7a7c21fb25c384127879ded5ed3b0a4'

TEST_ID = test_client.TEST_ID
TEST_KEY = test_client.TEST_KEY


class Result(object):
    def __init__(self, process_code, status_code=StatusCode.BadRequest):
        self._process_code = process_code
        self._status_code = status_code
    def validate(self, response):
        assert_equal(self._process_code, response.process_code)
        if isinstance(self._status_code, int):
            assert_equal(response.status_code, self._status_code)
        else:
            assert_in(response.status_code, self._status_code)
        if self._process_code is None:
            assert_is_none(response.output)
            assert_is_none(response.exc_info)
        elif response:
            assert_is_not_none(response.output)
            assert_is_none(response.exc_info)
        else:
            assert_is_none(response.output)
            assert_is_not_none(response.exc_info)
        return response

class Test(object):
    def __init__(self, args, result, pdf2img=None):
        self._args, self._result = (args, result)
        self._pdf2img = pdf2img if pdf2img else Test.pdf2img()
    def __call__(self, base_url=BASE_URL):
        return self._result.validate(self.post(base_url))
    def post(self, base_url):
        return self._pdf2img(['test'] + self._args, base_url)
    @classmethod
    def pdf2img(cls, id=TEST_ID, key=TEST_KEY):
        return test_client.pdf2img(id, key)
