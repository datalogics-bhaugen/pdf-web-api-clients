"server regression tests"

import test
from test import Result, Test
from test_client import ImageProcessCode as ProcessCode, StatusCode
from nose.tools import assert_in


def test_bad_version():
    result = Result(None, StatusCode.NotFound)
    try: Test(['data/bad.pdf'], result)(test.BASE_URL, 'spam')
    except Exception as exception:
        assert_in(max_retry_error('/api/spam/actions/image'), str(exception))

def test_bad_url():
    result = Result(ProcessCode.InvalidInput, StatusCode.BadRequest)
    try: Test(['http://127.0.0.1/spam.pdf'], result)()
    except Exception as exception:
        assert_in(max_retry_error('/spam.pdf'), str(exception))

def max_retry_error(url): return 'Max retries exceeded with url: %s' % url

def test_missing_url():
    pass  # TODO

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
    Test(['-password=spam', 'data/protected.pdf'], result)()

def test_adept_drm():
    result = Result(ProcessCode.AdeptDRM, StatusCode.Forbidden)
    Test(['data/ADEPT-DRM.pdf'], result)()

def test_insufficient_memory(): _memory_error('scripts/insufficient_memory')
def test_out_of_memory(): _memory_error('scripts/out_of_memory')

def _memory_error(mock_script):
    request_entity_too_large = StatusCode.RequestEntityTooLarge
    result = Result(ProcessCode.RequestTooLarge, request_entity_too_large)
    with test.MockPDF2IMG(mock_script):
        Test(['data/bad.pdf'], result)()

def test_pdf2img_crash():
    result = Result(ProcessCode.UnknownError, StatusCode.InternalServerError)
    with test.MockPDF2IMG('../bin/segfault'):
        Test(['data/bad.pdf'], result)()
