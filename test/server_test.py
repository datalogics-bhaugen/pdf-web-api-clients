"server regression tests"

import platform
import test
from test import Result, Test
from test_client import ImageProcessCode as ProcessCode, StatusCode
from nose.tools import assert_in


def linux_only(func):
    "enable/disable tests that require APDFL 10"
    func.__test__ = platform.system() == 'Linux'
    return func


def test_bad_version():
    result = Result(None, StatusCode.NotFound)
    try: Test(['data/bad.pdf'], result)('spam', test.BASE_URL)
    except Exception as exception:
        max_retries = 'Max retries exceeded with url: /api/spam/actions/image'
        assert_in(max_retries, str(exception))

def test_bad_pdf():
    result = Result(ProcessCode.InvalidInput, StatusCode.UnsupportedMediaType)
    Test(['data/bad.pdf'], result)()

def test_truncated_pdf():
    result = Result(ProcessCode.InvalidInput, StatusCode.BadRequest)
    Test(['data/truncated.pdf'], result)()

@linux_only
def test_missing_password():
    result = Result(ProcessCode.MissingPassword, StatusCode.Forbidden)
    Test(['data/protected.pdf'], result)()

@linux_only
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

