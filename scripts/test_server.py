"server regression tests"
# This file is set to help run regression tests on 
# the PDFL Web-API server.  This is to be run after
# changes to the server code to verify no issues 
# were created with previous code and/or pdf2img

import test_client
from nose.tools import assert_equal, assert_is_none


BASE_URL = 'http://127.0.0.1:5000'


def test_bad_version():
    pdf2img = test_client.pdf2img('api-key', -1, BASE_URL)
    response = pdf2img(['test', __file__, 'jpg'])
    assert_equal(response.status_code, 404)
    assert_is_none(response.process_code)
    assert_is_none(response.exc_info)
    assert_is_none(response.output)

# Tests to be made
# def test_arg_parsing():        #verify arg syntax to pdf2img
# def test_correct_syntax():     #verify input syntax errors
# def test_bmp_colormodel():     #verify BMP not RGB or Gray error
# def test_memory():             #verify insufficient memory error
# def test_color_model():        #verify color model error
# def test_output_type():        #verifies out type error
# def test_no_arguments():       #verifies no arguments error
# def test_page_range():         #verifies page range error
# def test_password_not_given(): #verifies password missing error
# def test_password_incorrect(): #verifes password incorrect error
# def test_drm_protection():     #verifes DRM protected file error
# def test_pdf_input():          #verifies input file not a pdf error
# def test_pdf2img():            #verifies handling of pdf2img crash
# def test_pdf_file_integrity(): #verifies truncated file error
# def test_png():                #verify output vs baseline png
# def test_jpg():                #verify output vs baseline jpg
# def test_bmp():                #verify output vs baseline bmp
# def test_tif():                #verify output vs baseline tif


