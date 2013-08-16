"server regression tests"

import test
from test import Result, Test
from test_client import ProcessCode, StatusCode


def test_bad_version():
    result = Result(None, StatusCode.NotFound)
    Test(['data/bad.pdf', 'jpg'], result).validate('spam', test.BASE_URL)

def test_bad_pdf():
    result = Result(ProcessCode.InvalidInput, StatusCode.UnsupportedMediaType)
    Test(['data/bad.pdf', 'jpg'], result).validate()

def test_truncated_pdf():
    result = Result(ProcessCode.InvalidInput, StatusCode.BadRequest)
    Test(['data/truncated.pdf', 'jpg'], result).validate()

def test_missing_password():
    result = Result(ProcessCode.MissingPassword, StatusCode.Forbidden)
    Test(['data/protected.pdf', 'jpg'], result).validate()

def test_invalid_password():
    result = Result(ProcessCode.InvalidPassword, StatusCode.Forbidden)
    Test(['-password=spam', 'data/protected.pdf', 'jpg'], result).validate()

def test_adept_drm():
    result = Result(ProcessCode.AdeptDRM, StatusCode.Forbidden)
    Test(['data/ADEPT-DRM.pdf', 'jpg'], result).validate()

def test_page_out_of_range():
    result = Result(ProcessCode.InvalidPage, StatusCode.BadRequest)
    Test(['-pages=5', 'data/four_pages.pdf', 'jpg'], result).validate()


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
# TODO: def test_invalid_region():
# TODO: def test_pdf2img_crash():

