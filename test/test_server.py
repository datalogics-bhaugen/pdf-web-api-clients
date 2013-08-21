"server regression tests"

import platform
import test
from test import Result, Test
from test_client import ProcessCode, StatusCode


def linux_only(func):
    "enable/disable tests that require pdf2img built with APDFL 10"
    func.__test__ = platform.system() == 'Linux'
    return func


def test_bad_version():
    result = Result(None, StatusCode.NotFound)
    Test(['data/bad.pdf'], result).validate('spam', test.BASE_URL)

def test_bad_pdf():
    result = Result(ProcessCode.InvalidInput, StatusCode.UnsupportedMediaType)
    Test(['data/bad.pdf'], result).validate()

def test_truncated_pdf():
    result = Result(ProcessCode.InvalidInput, StatusCode.BadRequest)
    Test(['data/truncated.pdf'], result).validate()

@linux_only
def test_missing_password():
    result = Result(ProcessCode.MissingPassword, StatusCode.Forbidden)
    Test(['data/protected.pdf'], result).validate()

@linux_only
def test_invalid_password():
    result = Result(ProcessCode.InvalidPassword, StatusCode.Forbidden)
    Test(['-password=spam', 'data/protected.pdf'], result).validate()

def test_adept_drm():
    result = Result(ProcessCode.AdeptDRM, StatusCode.Forbidden)
    Test(['data/ADEPT-DRM.pdf'], result).validate()

def test_page_out_of_range():
    result = Result(ProcessCode.InvalidPage, StatusCode.BadRequest)
    Test(['-pages=5', 'data/four_pages.pdf'], result).validate()

def test_insufficient_memory():
    request_entity_too_large = StatusCode.RequestEntityTooLarge
    result = Result(ProcessCode.RequestTooLarge, request_entity_too_large)
    with test.BackEnd('scripts/insufficient_memory') as insufficient_memory:
        Test(['data/bad.pdf'], result).validate()

def test_pdf2img_crash():
    result = Result(ProcessCode.UnknownError, StatusCode.InternalServerError)
    with test.BackEnd('scripts/program_crash') as pdf2img_crash:
        Test(['data/bad.pdf'], result).validate()
