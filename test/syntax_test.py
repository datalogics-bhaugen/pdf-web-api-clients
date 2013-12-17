"server regression tests, syntax"

import json
from test import Result, Test
from test_client import HTTPCode, RenderPages
from nose.tools import assert_equal


ERROR = "{} is not a valid '{}' value"
ErrorCode = RenderPages.ErrorCode

class SyntaxFixture(object):
    def validate(self, options, error_code=None):
        options = 'options={}'.format(json.dumps(options))
        result = Result(error_code) if error_code else self.result
        return Test(['data/four_pages.pdf', options], result)()

class TestColorModel(SyntaxFixture):
    def test_invalid_color_model(self):
        self.validate({'colorModel': 'spam'})
    def test_invalid_gif_color_model(self):
        self.validate({'outputFormat': 'gif', 'colorModel': 'cmyk'})
    @property
    def result(self): return Result(ErrorCode.InvalidColorModel)

class TestInvalidSyntax(SyntaxFixture):
    def test_invalid_flag(self):
        return  # TODO: restore when test drives server directly
        self.validate({'spam': True})
    def test_invalid_flag_value(self):
        test_result = self.validate({'printPreview': 'true'})
        error = 'invalid printPreview value: true'
        assert_equal(error, test_result.error_message)
    def test_another_invalid_flag_value(self):
        test_result = self.validate({'printPreview': 'True'})
        error = 'invalid printPreview value: True'
        assert_equal(error, test_result.error_message)
    def test_invalid_option(self):
        return  # TODO: restore when test drives server directly
        self.validate({'spam': 'spam'})
    def test_invalid_compression(self):
        self.validate({'compression': 'no'}, ErrorCode.InvalidCompression)
    def test_invalid_region(self):
        self.validate({'pdfRegion': 'spam'}, ErrorCode.InvalidRegion)
    @property
    def result(self): return Result(ErrorCode.InvalidSyntax)

class TestOutputFormat(SyntaxFixture):
    def test_invalid(self):
        self.validate({'outputFormat': 'spam'})
    def test_unsupported(self):
        self.validate({'outputFormat': 'raw'})
    def test_unsupported_multipage(self):
        self.validate({'outputFormat': 'jpg', 'pages': '1-2'})
    @property
    def result(self): return Result(ErrorCode.InvalidOutputFormat)

class TestPagesInvalid(SyntaxFixture):
    def test_invalid_pages(self):
        self.validate({'pages': 'spam'})
    def test_invalid_pages_type(self):
        error_message = self.validate({'pages': True}).error_message
        assert_equal(ERROR.format(True, 'pages'), error_message)
    def test_invalid_page_range(self):
        self.validate({'outputFormat': 'tif', 'pages': '1-2-3'})
    def test_inverted_page_range(self):
        self.validate({'outputFormat': 'tif', 'pages': '2-1'})
    def test_no_start_page(self):
        self.validate({'outputFormat': 'tif', 'pages': '-2'})
    def test_no_end_page(self):
        self.validate({'outputFormat': 'tif', 'pages': '1-'})
    def test_start_page_out_of_range(self):
        self.validate({'pages': '5'})
    def test_end_page_out_of_range(self):
        self.validate({'outputFormat': 'tif', 'pages': '1-5'})
    @property
    def result(self): return Result(ErrorCode.InvalidPage)

class TestResolutionInvalid(SyntaxFixture):
    def test_invalid_resolution_type(self): self._validate(False)
    def test_nonsquare_pixel(self): self._validate('300x300')
    def _validate(self, resolution):
        error_message = self.validate({'resolution': resolution}).error_message
        assert_equal(ERROR.format(resolution, 'resolution'), error_message)
    @property
    def result(self): return Result(ErrorCode.InvalidResolution)

class TestResultOK(SyntaxFixture):
    def test_last_page(self):
        self.validate({'pages': 'last'})
    def test_valid_page(self):
        self.validate({'pages': 2})
    def test_valid_page_list(self):
        self.validate({'outputFormat': 'tif', 'pages': '1,2,3'})
    def test_another_valid_page_list(self):
        self.validate({'outputFormat': 'tif', 'pages': '3,2,1'})
    def test_valid_page_range(self):
        self.validate({'outputFormat': 'tif', 'pages': '1-2'})
    def test_valid_resolution(self):
        self.validate({'resolution': 200})
    @property
    def result(self): return Result()
