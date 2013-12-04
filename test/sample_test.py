"WebAPI regression tests"

import os
import glob
import platform
import subprocess
from server.tmpdir import Stdout
from test_client import ErrorCode
from nose.tools import assert_equal, assert_in


GOOD_PDF = 'data/four_pages.pdf'
INPUT_URL = 'http://www.datalogics.com/pdf/doc/pdf2img.pdf'
PERL_ARGS = ['pdfprocess/perl', 'RenderPages']


def set_python_path():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    eggs_dir = os.path.join(root_dir, 'eggs')
    requests_dir = glob.glob(os.path.join(eggs_dir, 'requests-*.egg'))[0]
    os.environ['PYTHONPATH'] = requests_dir

def test_pdf2img_application():
    args = ['pdf2img', 'data/hello_world.pdf', 'tif']
    with Stdout() as stdout:
        assert_equal(subprocess.call(args, stdout=stdout), 0)
        assert_in('PDF2IMG', str(stdout))

def test_pdfprocess_sample_perl():
    perl_sample = '../samples/perl/pdfprocess.pl'
    args = [perl_sample, 'RenderPages', 'data/bad.pdf', 'unused.png']
    with Stdout() as stdout:
        error_code = subprocess.call(args, stdout=stdout)
        assert_equal(error_code, ErrorCode.AuthorizationError)
        assert_in('your app id', str(stdout))

def test_pdfprocess_sample_perl_patched():
    args = PERL_ARGS + [GOOD_PDF, 'four_pages.png']
    with Stdout() as stdout:
        assert_equal(subprocess.call(args, stdout=stdout), 0)

def test_pdfprocess_sample_perl_patched_url():
    args = PERL_ARGS + [INPUT_URL, 'four_pages.png']
    with Stdout() as stdout:
        assert_equal(subprocess.call(args, stdout=stdout), 0)

def test_pdfprocess_sample_python(python3=False):
    args = ['../samples/python/pdfprocess.py', 'RenderPages', 'data/bad.pdf']
    validate_sample_python(args, 'your app id', python3)

def test_pdfprocess_sample_python_patched(python3=False):
    args = ['pdfprocess/python', 'RenderPages', GOOD_PDF]
    validate_sample_python(args, 'created: data/four_pages.png', python3)

def test_pdfprocess_sample_python_patched_url(python3=False):
    args = ['pdfprocess/python', 'RenderPages', INPUT_URL]
    validate_sample_python(args, 'created: pdf2img.png', python3)

def validate_sample_python(args, output, python3):
    set_python_path()
    if python3: args[0:0] = ['python3']
    with Stdout() as stdout:
        assert_equal(subprocess.call(args, stdout=stdout), 0)
        assert_in(output, str(stdout))

if platform.system() == 'Darwin':
    def test_pdfprocess_sample_php():
        php_sample = '../samples/php/pdfprocess.php'
        args = ['php', php_sample, 'RenderPages', 'data/bad.pdf']
        with Stdout() as stdout:
            error_code = subprocess.call(args, stdout=stdout)
            assert_equal(error_code, ErrorCode.AuthorizationError)
            assert_in('your app id', str(stdout))

    def test_pdfprocess_sample_php_patched():
        args = ['php', 'pdfprocess/php', 'RenderPages', GOOD_PDF]
        with Stdout() as stdout:
            assert_equal(subprocess.call(args, stdout=stdout), 0)

    def test_pdfprocess_sample_php_patched_url():
        args = ['php', 'pdfprocess/php', 'RenderPages', INPUT_URL]
        with Stdout() as stdout:
            assert_equal(subprocess.call(args, stdout=stdout), 0)

    def test_pdfprocess_sample_python3():
        test_pdfprocess_sample_python(python3=True)

    def test_pdfprocess_sample_python3_patched():
        test_pdfprocess_sample_python_patched(python3=True)

    def test_pdfprocess_sample_python3_patched_url():
        test_pdfprocess_sample_python_patched_url(python3=True)
