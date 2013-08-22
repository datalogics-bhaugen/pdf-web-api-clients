"server regression tests, syntax"

from test import Result, Test
from test_client import ImageProcessCode as ProcessCode, StatusCode


def test_missing_equals():
    result = Result(ProcessCode.InvalidSyntax, StatusCode.BadRequest)
    Test(['-pages', 'data/four_pages.pdf'], result)()

def test_missing_value():
    result = Result(ProcessCode.InvalidSyntax, StatusCode.BadRequest)
    Test(['-pages=', 'data/four_pages.pdf'], result)()

def test_invalid_flag():
    result = Result(ProcessCode.InvalidSyntax, StatusCode.BadRequest)
    Test(['-spam', 'data/four_pages.pdf'], result)()

def test_invalid_option():
    result = Result(ProcessCode.InvalidSyntax, StatusCode.BadRequest)
    Test(['-spam=spam', 'data/four_pages.pdf'], result)()

def test_invalid_output_type():
    result = Result(ProcessCode.InvalidOutputType, StatusCode.BadRequest)
    Test(['-outputForm=spam', 'data/four_pages.pdf'], result)()

def test_unsupported_output_type():
    result = Result(ProcessCode.InvalidOutputType, StatusCode.BadRequest)
    Test(['-outputForm=raw', 'data/four_pages.pdf'], result)()

def test_unsupported_multipage_output_type():
    result = Result(ProcessCode.InvalidOutputType, StatusCode.BadRequest)
    Test(['-outputForm=jpg', '-pages=1-2', 'data/four_pages.pdf'], result)()

def test_invalid_pages():
    result = Result(ProcessCode.InvalidPage, StatusCode.BadRequest)
    Test(['-pages=spam', 'data/four_pages.pdf'], result)()

def test_invalid_page_range():
    result = Result(ProcessCode.InvalidPage, StatusCode.BadRequest)
    Test(['-pages=1-2-3', 'data/four_pages.pdf'], result)()

def test_start_page_out_of_range():
    result = Result(ProcessCode.InvalidPage, StatusCode.BadRequest)
    Test(['-pages=5', 'data/four_pages.pdf'], result)()

def test_end_page_out_of_range():
    result = Result(ProcessCode.InvalidPage, StatusCode.BadRequest)
    Test(['-pages=1-5', 'data/four_pages.pdf'], result)()

def test_bad_color_model():
    result = Result(ProcessCode.InvalidColorModel, StatusCode.BadRequest)
    Test(['-colorModel=spam', 'data/four_pages.pdf'], result)()

def test_bad_gif_color_model():
    args = ['-outputForm=gif', '-colorModel=cmyk', 'data/four_pages.pdf']
    result = Result(ProcessCode.InvalidColorModel, StatusCode.BadRequest)
    Test(args, result)()

def test_bad_compression():
    result = Result(ProcessCode.InvalidCompression, StatusCode.BadRequest)
    Test(['-compression=spam', 'data/four_pages.pdf'], result)()

def test_invalid_region():
    result = Result(ProcessCode.InvalidRegion, StatusCode.BadRequest)
    Test(['-pdfregion=spam', 'data/four_pages.pdf'], result)()

def test_invalid_resolution():
    result = Result(ProcessCode.InvalidResolution, StatusCode.BadRequest)
    Test(['-resolution=300x300', 'data/four_pages.pdf'], result)()

