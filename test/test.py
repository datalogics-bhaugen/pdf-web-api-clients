"server test classes"

import test_client
from nose.tools import assert_equal, assert_is_none, assert_is_not_none


APPLICATION_ID = test_client.APPLICATION_ID
APPLICATION_KEY = test_client.APPLICATION_KEY
BASE_URL = 'http://127.0.0.1:5000'
VERSION = test_client.VERSION


class Result(object):
    def __init__(self, process_code, status_code):
        self._process_code = process_code
        self._status_code = status_code
    def validate(self, response):
        assert_equal(self._process_code, response.process_code)
        assert_equal(self._status_code, response.status_code)
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
    def validate(self, version=VERSION, base_url=BASE_URL):
        response = self._pdf2img(version, base_url, self._args)
        self._result.validate(response)
    @classmethod
    def pdf2img(cls, id=APPLICATION_ID, key=APPLICATION_KEY):
        return test_client.pdf2img(id, key)

