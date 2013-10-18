"server regression tests"

import mock
import test
from test import Result, Test
from test_client import ProcessCode, StatusCode
from nose.tools import assert_in


def test_bad_url():
    errors = (StatusCode.BadRequest, StatusCode.UnsupportedMediaType)
    result = Result(ProcessCode.InvalidInput, errors)
    try: Test(['http://127.0.0.1/spam.pdf'], result)()
    except Exception as exception:
        assert_in(max_retry_error('/spam.pdf'), str(exception))

def max_retry_error(url):
    return 'Max retries exceeded with url: {}'.format(url)

def test_good_url():
    result = Result(ProcessCode.OK, StatusCode.OK)
    Test(['http://www.datalogics.com/pdf/doc/pdf2img.pdf'], result)()

def test_bad_pdf():
    result = Result(ProcessCode.InvalidInput, StatusCode.UnsupportedMediaType)
    Test(['data/bad.pdf'], result)()

def test_truncated_pdf():
    result = Result(ProcessCode.InvalidInput, StatusCode.BadRequest)
    Test(['data/truncated.pdf'], result)()

def test_missing_password():
    result = Result(ProcessCode.MissingPassword, StatusCode.Forbidden)
    Test(['data/protected.pdf'], result)()

def test_invalid_password():
    result = Result(ProcessCode.InvalidPassword, StatusCode.Forbidden)
    Test(['data/protected.pdf', 'password=spam'], result)()

def test_adept_drm():
    result = Result(ProcessCode.AdeptDRM, StatusCode.Forbidden)
    Test(['data/ADEPT-DRM.pdf'], result)()

def test_insufficient_memory(): _memory_error('scripts/insufficient_memory')
def test_out_of_memory(): _memory_error('scripts/out_of_memory')

def _memory_error(mock_script):
    request_entity_too_large = StatusCode.RequestEntityTooLarge
    result = Result(ProcessCode.RequestTooLarge, request_entity_too_large)
    with mock.Client(mock_script):
        Test(['data/bad.pdf'], result)()

def test_pdf2img_crash():
    result = Result(ProcessCode.UnknownError, StatusCode.InternalServerError)
    with mock.Client('../bin/segfault'):
        Test(['data/bad.pdf'], result)()
