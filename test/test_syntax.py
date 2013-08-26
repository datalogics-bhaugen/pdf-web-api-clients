"server regression tests, syntax"

from test import Result, Test
from test_client import ImageProcessCode as ProcessCode, StatusCode


class TestColorModel:
    def test_bad_color_model(self):
        Test(['-colorModel=spam', 'data/four_pages.pdf'], self.result)()
    def test_bad_gif_color_model(self):
        args = ['-outputForm=gif', '-colorModel=cmyk', 'data/four_pages.pdf']
        Test(args, self.result)()
    @property
    def result(self): return Result(ProcessCode.InvalidColorModel)

class TestInvalidSyntax:
    def test_missing_equals(self):
        Test(['-pages', 'data/four_pages.pdf'], self.result)()
    def test_missing_value(self):
        Test(['-pdfRegion=', 'data/four_pages.pdf'], self.result)()
    def test_invalid_flag(self):
        Test(['-spam', 'data/four_pages.pdf'], self.result)()
    def test_invalid_option(self):
        Test(['-spam=spam', 'data/four_pages.pdf'], self.result)()
    def test_invalid_compression(self):
        result = Result(ProcessCode.InvalidCompression)
        Test(['-compression=spam', 'data/four_pages.pdf'], result)()
    def test_invalid_region(self):
        result = Result(ProcessCode.InvalidRegion)
        Test(['-pdfregion=spam', 'data/four_pages.pdf'], result)()
    def test_invalid_resolution(self):
        result = Result(ProcessCode.InvalidResolution)
        Test(['-resolution=300x300', 'data/four_pages.pdf'], result)()
    @property
    def result(self): return Result(ProcessCode.InvalidSyntax)

class TestOutputType:
    def test_invalid(self):
        Test(['-outputForm=spam', 'data/four_pages.pdf'], self.result)()
    def test_unsupported(self):
        Test(['-outputForm=raw', 'data/four_pages.pdf'], self.result)()
    def test_unsupported_multipage(self):
        args = ['-outputForm=jpg', '-pages=1-2', 'data/four_pages.pdf']
        Test(args, self.result)()
    @property
    def result(self): return Result(ProcessCode.InvalidOutputType)

class TestPagesInvalid: # TODO: remove some of these?
    def test_invalid_pages(self):
        Test(['-pages=spam', 'data/four_pages.pdf'], self.result)()
    def test_invalid_page_range(self):
        Test(['-pages=1-2-3', 'data/four_pages.pdf'], self.result)()
    def test_inverted_page_range(self):
        Test(['-pages=2-1', 'data/four_pages.pdf'], self.result)()
    def test_no_start_page(self):
        Test(['-pages=-2', 'data/four_pages.pdf'], self.result)()
    def test_no_end_page(self):
        Test(['-pages=1-', 'data/four_pages.pdf'], self.result)()
    def test_start_page_out_of_range(self):
        Test(['-pages=5', 'data/four_pages.pdf'], self.result)()
    def test_end_page_out_of_range(self):
        Test(['-pages=1-5', 'data/four_pages.pdf'], self.result)()
    @property
    def result(self): return Result(ProcessCode.InvalidPage)

class TestPagesOK: # TODO: remove some of these?
    def test_last_page(self):
        Test(['-pages=last', 'data/four_pages.pdf'], self.result)()
    def test_valid_page(self):
        Test(['-pages=2', 'data/four_pages.pdf'], self.result)()
    def test_valid_page_list(self):
        Test(['-pages=1,2,3', 'data/four_pages.pdf'], self.result)()
    def test_another_valid_page_list(self):
        Test(['-pages=3,2,1', 'data/four_pages.pdf'], self.result)()
    def test_valid_page_range(self):
        Test(['-pages=1-2', 'data/four_pages.pdf'], self.result)()
    @property
    def result(self): return Result(ProcessCode.OK, StatusCode.OK)

