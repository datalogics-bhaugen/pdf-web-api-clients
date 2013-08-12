"server regression tests"

import test_client
from nose.tools import assert_equal, assert_is_none, assert_is_not_none


API_KEY = test_client.API_KEY
BASE_URL = test_client.BASE_URL
VERSION = test_client.VERSION

BAD_API_KEY = '5184f74f1e1917913e6adcc31b0c3b9c'


class Result(object):
    def __init__(self, status_code, process_code):
        self._status_code = status_code
        self._process_code = process_code
    def validate(self, response):
        assert_equal(self._status_code, response.status_code)
        assert_equal(self._process_code, response.process_code)
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
    Test(['../test/bad.pdf', 'jpg'], Result(404, None), pdf2img).validate()

def test_pdf_input():
    Test(['../test/bad.pdf', 'tif'], Result(422, 233)).validate()

def test_drm_protection():
    Test(['../test/ADEPT-DRM.pdf', 'tif'], Result(403, 233)).validate()

def test_pdf_file_integrity():
    Test(['../test/truncated.pdf', 'tif'], Result(422, 233)).validate()

def test_no_arguments():
    Test([], Result(417, 1)).validate()
    

# TODO: more tests
# def test_arg_parsing():        #verify arg syntax to pdf2img
# def test_correct_syntax():     #verify input syntax errors
# def test_bmp_colormodel():     #verify BMP not RGB or Gray error
# def test_memory():             #verify insufficient memory error
# def test_color_model():        #verify color model error
# def test_output_type():        #verifies out type error
# def test_page_range():         #verifies page range error
# def test_password_not_given(): #verifies password missing error
# def test_password_incorrect(): #verifes password incorrect error
# def test_pdf2img():            #verifies handling of pdf2img crash
# def test_png():                #verify output vs baseline png
# def test_jpg():                #verify output vs baseline jpg
# def test_bmp():                #verify output vs baseline bmp
# def test_tif():                #verify output vs baseline tif

