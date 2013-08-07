"server regression tests"

import test_client
from nose.tools import assert_equal, assert_is_none, assert_is_not_none


API_KEY = 'f54ab5d8-5775-42c7-b888-f074ba892b57'
BASE_URL = 'http://127.0.0.1:5000'
VERSION = 0

class Result(object):
    def __init__(self, status_code, process_code):
        self._status_code = status_code
        self._process_code = process_code
    def validate(self, response):
        assert_equal(self._status_code, response.status_code)
        assert_equal(self._process_code, response.process_code)
        if self._process_code is None:
            assert_is_none(response.output)
            assert_is_none(response.exc_info)
        elif response:
            assert_is_not_none(response.output)
            assert_is_none(response.exc_info)
        else:
            assert_is_none(response.output)
            assert_is_not_none(response.exc_info)

class Test(object):
    def __init__(self, args, result, pdf2img=None):
        self._args = ['test'] + args
        self._result = result
        self._pdf2img = pdf2img if pdf2img else Test.pdf2img()
    def validate(self):
        response = self._pdf2img(self._args)
        self._result.validate(response)
    @classmethod
    def pdf2img(cls, api_key=API_KEY, version=VERSION, base_url=BASE_URL):
        return test_client.pdf2img(api_key, version, base_url)


def test_bad_version():
    args = [__file__, 'jpg']
    result = Result(404, None)
    Test(args, result, Test.pdf2img('api-key', -1, BASE_URL)).validate()

# TODO: more tests

