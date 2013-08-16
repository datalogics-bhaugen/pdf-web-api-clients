"server regression tests, syntax"

from test import Result, Test
from test_client import ImageProcessCode, ProcessCode, StatusCode


def test_invalid_output_type():
    result = Result(ProcessCode.InvalidOutputType, StatusCode.BadRequest)
    Test(['data/four_pages.pdf', 'spam'], result).validate()

def test_invalid_pages():
    result = Result(ProcessCode.InvalidPage, StatusCode.BadRequest)
    Test(['-pages=spam', 'data/four_pages.pdf', 'jpg'], result).validate()

def test_upper_case():
    result = Result(ProcessCode.InvalidPage, StatusCode.BadRequest)
    Test(['-PAGES=5', 'data/four_pages.pdf', 'jpg'], result).validate()

def test_lower_case():
    result = Result(ProcessCode.OK, StatusCode.OK)
    Test(['-opp', 'data/four_pages.pdf', 'jpg'], result).validate()

def test_missing_equals():
    result = Result(ProcessCode.InvalidSyntax, StatusCode.BadRequest)
    Test(['-pages', 'data/four_pages.pdf', 'jpg'], result).validate

def test_missing_value():
    result = Result(ProcessCode.InvalidSyntax, StatusCode.BadRequest)
    Test(['-pages=', 'data/four_pages.pdf', 'jpg'], result).validate

def test_bad_color_model():
    args = ['-colorModel=spam', 'data/four_pages.pdf', 'jpg']
    result = Result(ImageProcessCode.InvalidColorModel, StatusCode.BadRequest)
    Test(args, result).validate()

def test_bad_compression():
    args = ['-compression=spam', 'data/four_pages.pdf', 'jpg']
    result = Result(ImageProcessCode.InvalidCompression, StatusCode.BadRequest)
    Test(args, result).validate()

def test_invalid_region():
    args = ['-pdfregion=spam', 'data/four_pages.pdf', 'jpg']
    result = Result(ImageProcessCode.InvalidRegion, StatusCode.BadRequest)
    Test(args, result).validate

