"server regression tests, options"

import test
from test_client import ProcessCode, StatusCode
from nose.tools import assert_in, assert_not_in


class MockFixture(object):
    @classmethod
    def setup_class(cls):
        cls.mock = test.Mock('scripts/options_test')
    @classmethod
    def teardown_class(cls):
        cls.mock = None
    @classmethod
    def validate(cls, options, expected, unexpected=None):
        ok = test.Result(ProcessCode.OK, StatusCode.OK)
        response = test.Test(options + ['data/four_pages.pdf'], ok)()
        output = response.output.rstrip().split(' ')
        if expected: assert_in(expected, output)
        if unexpected: assert_not_in(unexpected, output)

class TestAliases(MockFixture):
    def test_asprinted(self):
        self.validate(['-printPreview'], '-asprinted')
    def test_noannot(self):
        self.validate(['-suppressAnnotations'], '-noannot')
    def test_nocmm(self):
        self.validate(['-disableColorManagement'], '-nocmm')
    def test_noenhancethinlines(self):
        self.validate(['-disableThinLineEnhancement'], '-noenhancethinlines')
    def test_width(self):
        self.validate(['-width=1'], '-pixelcount=w:1')
    def test_height(self):
        self.validate(['-height=1'], '-pixelcount=h:1')
    def test_width_and_height(self):
        self.validate(['-width=1', '-height=1'], '-pixelcount=1x1')

class TestDefaults(MockFixture):
    def test_output_form(self):
        self.validate([], 'tif')
    def test_pages(self):
        self.validate(['-outputForm=jpg'], '-pages=1')
    def test_smoothing_all(self):
        self.validate([], '-smoothing=all')
    def test_smoothing_none(self):
        self.validate(['-Smoothing=none'], None, '-smoothing=none')
    def test_smoothing_text(self):
        self.validate(['-smoothing=text'], '-smoothing=text')

class TestSpelling(MockFixture):
    def test_lower_case(self):
        self.validate(['-opp'], '-OPP')
    def test_upper_case(self):
        self.validate(['-outputForm=jpg', '-PAGES=1'], '-pages=1')
    def test_jpeg(self):
        self.validate(['-outputForm=jpeg'], 'jpg')
    def test_tiff(self):
        self.validate(['-outputForm=tiff'], 'tif')

