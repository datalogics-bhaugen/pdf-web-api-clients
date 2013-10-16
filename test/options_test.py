"server regression tests, options"

import simplejson as json
import mock
import test
from test_client import ProcessCode, StatusCode
from nose.tools import assert_in, assert_not_in


class TestFixture(object):
    @classmethod
    def setup_class(cls):
        cls.mock = mock.Client('scripts/options_test')
    @classmethod
    def teardown_class(cls):
        cls.mock = None
    @classmethod
    def validate(cls, options, expected, unexpected=None):
        options = 'options=%s' % json.dumps(options)
        args = ['data/four_pages.pdf', options]
        ok = test.Result(ProcessCode.OK, StatusCode.OK)
        output = test.Test(args, ok)().output.rstrip().split(' ')
        if expected: assert_in(expected, output)
        if unexpected: assert_not_in(unexpected, output)

class TestAliases(TestFixture):
    def test_asprinted(self):
        self.validate({'printPreview': True}, '-asprinted')
    def test_noannot(self):
        self.validate({'suppressAnnotations': True}, '-noannot')
    def test_nocmm(self):
        self.validate({'disableColorManagement': True}, '-nocmm')
    def test_noenhancethinlines(self):
        options = {'disableThinLineEnhancement': True}
        self.validate(options, '-noenhancethinlines')
    def test_width(self):
        self.validate({'imageWidth': 1}, '-pixelcount=w:1')
    def test_height(self):
        self.validate({'imageHeight': 1}, '-pixelcount=h:1')
    def test_width_and_height(self):
        self.validate({'imageWidth': 1, 'imageHeight': 1}, '-pixelcount=1x1')

class TestDefaults(TestFixture):
    def test_multipage(self):
        self.validate({}, '-multipage')
    def test_output_form(self):
        self.validate({}, 'tif')
    def test_pages(self):
        self.validate({'outputForm': 'jpg'}, '-pages=1')
    def test_smoothing_all(self):
        self.validate({}, '-smoothing=all')
    def test_smoothing_none(self):
        self.validate({'Smoothing': 'none'}, None, '-smoothing=none')
    def test_smoothing_text(self):
        self.validate({'smoothing': 'text'}, '-smoothing=text')

class TestSpelling(TestFixture):
    def test_lower_case(self):
        self.validate({'opp': True}, '-OPP')
    def test_upper_case(self):
        self.validate({'outputForm': 'jpg', 'PAGES': '1'}, '-pages=1')
    def test_jpeg(self):
        self.validate({'outputForm': 'jpeg'}, 'jpg')
    def test_tiff(self):
        self.validate({'outputForm': 'tiff'}, 'tif')
