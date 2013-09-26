"server test classes"

import os
import sys
import subprocess
import test_client
from test_client import StatusCode
from nose.tools import assert_equal, assert_is_none, assert_is_not_none


BASE_URL = 'http://127.0.0.1:5000'
VERSION = test_client.VERSION

PUBLIC_ID = 'c953bc0d'
PUBLIC_KEY = 'c7a7c21fb25c384127879ded5ed3b0a4'

TEST_ID = test_client.TEST_ID
TEST_KEY = test_client.TEST_KEY


class MockLogger:
    def __init__(self):
        self._log = []
    def __getattr__(self, name):
        if name.startswith('_'): raise AttributeError(name)
        def log(value): self._log.append((name, value))
        return log
    @property
    def log(self): return self._log


class MockPDF2IMG(object):
    def __init__(self, mock, pdf2img='pdf2img'):
        self._set_pdf2img(pdf2img)
        if not self.pdf2img: sys.exit('no %s in PATH' % pdf2img)
        self._set_temporary_name(pdf2img)
        subprocess.call(['mv', self.pdf2img, self.temporary_name])
        subprocess.call(['ln', '-s', os.path.abspath(mock), self.pdf2img])
    def __del__(self):
        subprocess.call(['mv', self.temporary_name, self.pdf2img])
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        pass
    def _set_pdf2img(self, pdf2img):
        for dir in os.environ['PATH'].split(os.pathsep):
            filename = os.path.join(dir, pdf2img)
            if os.path.isfile(filename) and os.access(filename, os.X_OK):
                self._pdf2img = filename
    def _set_temporary_name(self, pdf2img):
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pdf2img_basename = os.path.basename(pdf2img)
        self._temporary_name = os.path.join(root_dir, 'bin', pdf2img_basename)
    @property
    def pdf2img(self): return self._pdf2img
    @property
    def temporary_name(self): return self._temporary_name


class MockRequest(object):
    def __init__(self, options):
        self._options = options
    @property
    def files(self): return {'spam': 0}
    @property
    def form(self): return {'options': self._options}
    @property
    def remote_addr(self): return 'localhost'


class Result(object):
    def __init__(self, process_code, status_code=StatusCode.BadRequest):
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
        return response


class Test(object):
    def __init__(self, args, result, pdf2img=None):
        self._args, self._result = (args, result)
        self._pdf2img = pdf2img if pdf2img else Test.pdf2img()
    def __call__(self, version=VERSION, base_url=BASE_URL):
        return self._result.validate(self.post(version, base_url))
    def post(self, version, base_url):
        return self._pdf2img(version, base_url, ['test'] + self._args)
    @classmethod
    def pdf2img(cls, id=TEST_ID, key=TEST_KEY):
        return test_client.pdf2img(id, key)
