"server regression tests, syntax"

import simplejson as json
from test import Result, Test
from test_client import RenderPagesProcessCode as ProcessCode, StatusCode
from nose.tools import assert_in


class SyntaxFixture(object):
    def validate(self, options, process_code=None):
        options = 'options=%s' % json.dumps(options)
        result = Result(process_code) if process_code else self.result
        return Test(['data/four_pages.pdf', options], result)()

class TestColorModel(SyntaxFixture):
    def test_invalid_color_model(self):
        self.validate({'colorModel': 'spam'})
    def test_invalid_gif_color_model(self):
        self.validate({'outputForm': 'gif', 'colorModel': 'cmyk'})
    @property
    def result(self): return Result(ProcessCode.InvalidColorModel)

class TestInvalidSyntax(SyntaxFixture):
    def test_invalid_flag(self):
        self.validate({'spam': True})
    def test_invalid_flag_value(self):
        error = 'invalid printPreview value: true'
        assert_in(error, self.validate({'printPreview': 'true'}).exc_info)
    def test_invalid_option(self):
        self.validate({'spam': 'spam'})
    def test_invalid_compression(self):
        self.validate({'compression': 'spam'}, ProcessCode.InvalidCompression)
    def test_invalid_region(self):
        self.validate({'pdfregion': 'spam'}, ProcessCode.InvalidRegion)
    def test_invalid_resolution(self):
        self.validate({'resolution': '300x300'}, ProcessCode.InvalidResolution)
    @property
    def result(self): return Result(ProcessCode.InvalidSyntax)

class TestOutputType(SyntaxFixture):
    def test_invalid(self):
        self.validate({'outputForm': 'spam'})
    def test_unsupported(self):
        self.validate({'outputForm': 'raw'})
    def test_unsupported_multipage(self):
        self.validate({'outputForm': 'jpg', 'pages': '1-2'})
    @property
    def result(self): return Result(ProcessCode.InvalidOutputType)

class TestPagesInvalid(SyntaxFixture):
    def test_invalid_pages(self):
        self.validate({'pages': 'spam'})
    def test_invalid_page_range(self):
        self.validate({'pages': '1-2-3'})
    def test_inverted_page_range(self):
        self.validate({'pages': '2-1'})
    def test_no_start_page(self):
        self.validate({'pages': '-2'})
    def test_no_end_page(self):
        self.validate({'pages': '1-'})
    def test_start_page_out_of_range(self):
        self.validate({'pages': '5'})
    def test_end_page_out_of_range(self):
        self.validate({'pages': '1-5'})
    @property
    def result(self): return Result(ProcessCode.InvalidPage)

class TestPagesOK(SyntaxFixture):
    def test_last_page(self):
        self.validate({'pages': 'last'})
    def test_valid_page(self):
        self.validate({'pages': '2'})
    def test_valid_page_list(self):
        self.validate({'pages': '1,2,3'})
    def test_another_valid_page_list(self):
        self.validate({'pages': '3,2,1'})
    def test_valid_page_range(self):
        self.validate({'pages': '1-2'})
    @property
    def result(self): return Result(ProcessCode.OK, StatusCode.OK)
