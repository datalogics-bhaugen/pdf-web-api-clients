"server regression tests"

import mock
import test
from test import Result, Test
from test_client import ErrorCode, HTTPCode
from nose.tools import assert_in


def test_bad_url():
    errors = (HTTPCode.BadRequest, HTTPCode.UnsupportedMediaType)
    result = Result(ErrorCode.InvalidInput, errors)
    try: Test(['http://127.0.0.1/spam.pdf'], result)()
    except Exception as exception:
        assert_in(max_retry_error('/spam.pdf'), str(exception))

def max_retry_error(url):
    return 'Max retries exceeded with url: {}'.format(url)

def test_flatten_form():
    args = ['data/annotated_form.pdf', 'input_name=annotated_form.pdf']
    Test(args, Result())('http://127.0.0.1:8080', 'flatten/form')

def test_good_url():
    Test(['http://www.datalogics.com/pdf/doc/pdf2img.pdf'], Result())()

def test_bad_pdf():
    result = Result(ErrorCode.InvalidInput, HTTPCode.UnsupportedMediaType)
    Test(['data/bad.pdf'], result)()

def test_truncated_pdf():
    result = Result(ErrorCode.InvalidInput, HTTPCode.BadRequest)
    Test(['data/truncated.pdf'], result)()

def test_missing_password():
    result = Result(ErrorCode.MissingPassword, HTTPCode.Forbidden)
    Test(['data/protected.pdf'], result)()

def test_invalid_password():
    result = Result(ErrorCode.InvalidPassword, HTTPCode.Forbidden)
    Test(['data/protected.pdf', 'password=spam'], result)()

def test_adept_drm():
    result = Result(ErrorCode.AdeptDRM, HTTPCode.Forbidden)
    Test(['data/ADEPT-DRM.pdf'], result)()

def test_insufficient_memory(): _memory_error('scripts/insufficient_memory')
def test_out_of_memory(): _memory_error('scripts/out_of_memory')

def _memory_error(mock_script):
    request_entity_too_large = HTTPCode.RequestEntityTooLarge
    result = Result(ErrorCode.RequestTooLarge, request_entity_too_large)
    with mock.Client(mock_script):
        Test(['data/bad.pdf'], result)()

def test_pdf2img_crash():
    result = Result(ErrorCode.UnknownError, HTTPCode.InternalServerError)
    with mock.Client('../bin/segfault'):
        Test(['data/bad.pdf'], result)()
