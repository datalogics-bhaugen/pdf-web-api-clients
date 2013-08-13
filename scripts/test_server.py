"server regression tests"

import test_client
from test_client import ProcessCode, StatusCode
from nose.tools import assert_equal, assert_is_none, assert_is_not_none


API_KEY = test_client.API_KEY
BASE_URL = test_client.BASE_URL
VERSION = test_client.VERSION

BAD_API_KEY = '5184f74f1e1917913e6adcc31b0c3b9c'


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
    def validate(self):
        response = self._pdf2img(self._args)
        self._result.validate(response)
    @classmethod
    def pdf2img(cls, api_key=API_KEY, version=VERSION, base_url=BASE_URL):
        return test_client.pdf2img(api_key, version, base_url)


def test_bad_version():
    pdf2img = Test.pdf2img('api-key', -1, BASE_URL)
    result = Result(None, StatusCode.NotFound)
    Test(['../test/bad.pdf', 'jpg'], result, pdf2img).validate()

def test_bad_pdf():
    result = Result(ProcessCode.InvalidInput, StatusCode.UnsupportedMediaType)
    Test(['../test/bad.pdf', 'jpg'], result).validate()

def test_truncated_pdf():
    result = Result(ProcessCode.InvalidInput, StatusCode.BadRequest)
    Test(['../test/truncated.pdf', 'jpg'], result).validate()

def test_missing_password():
    result = Result(ProcessCode.MissingPassword, StatusCode.Forbidden)
    Test(['../test/protected.pdf', 'jpg'], result).validate()

def test_invalid_password():
    result = Result(ProcessCode.InvalidPassword, StatusCode.Forbidden)
    Test(['-password=spam', '../test/protected.pdf', 'jpg'], result).validate()

def test_adept_drm():
    result = Result(ProcessCode.AdeptDRM, StatusCode.Forbidden)
    Test(['../test/ADEPT-DRM.pdf', 'jpg'], result).validate()

def test_invalid_output_type():
    result = Result(ProcessCode.InvalidOutputType, StatusCode.BadRequest)
    Test(['../test/four_pages.pdf', 'spam'], result).validate()

def test_invalid_pages():
    result = Result(ProcessCode.InvalidPage, StatusCode.BadRequest)
    Test(['-pages=spam', '../test/four_pages.pdf', 'jpg'], result).validate()

def test_page_out_of_range():
    result = Result(ProcessCode.InvalidPage, StatusCode.BadRequest)
    Test(['-pages=5', '../test/four_pages.pdf', 'jpg'], result).validate()


# unused pdf2img error codes:
# ERR_NOERROR
# ERR_SYNTAX

# pdf2img error codes for command-line syntax errors that cannot happen:
# ERR_BPS_NOT_VALID
# ERR_MAX_BAND_MEM_INVALID
# ERR_NO_PERMISSION
# ERR_OUTPUTFILE
# ERR_QUALITY_INVALID
# ERR_RESOLUTION_INVALID

# pdf2img error codes, values (subtract 768 from #define value), and meaning:
# ERR_INPUTFILE                 233     cannot open (various reasons)
# ERR_COMPRESSION_INVALID       236     value unrecognized
# ERR_COLORSPACE_NOT_VALID      237     value unrecognized
# ERR_OUTPUT_TYPE_INVALID       239     value unrecognized, e.g. 'bmp'
# ERR_UNDEFINED_PAGE            241     value unrecognized, or out of range
# ERR_MEMORY                    243     too many pages
# ERR_REGION_INVALID            244     value unrecognized

# TODO: def test_insufficient_memory():
# TODO: def test_invalid_color_space():
# TODO: def test_invalid_compression():
# TODO: def test_invalid_region():
# TODO: def test_pdf2img_crash():

