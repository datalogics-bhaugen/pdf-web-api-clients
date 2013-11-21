"WebAPI regression tests"

import os
import glob
import platform
import subprocess
from server.tmpdir import Stdout
from test_client import ErrorCode
from nose.tools import assert_equal, assert_in


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

def test_pdfprocess_sample_php():
    args = ['../samples/php/pdfprocess.php', 'RenderPages', 'data/bad.pdf']
    with Stdout() as stdout:
        error_code = subprocess.call(args, stdout=stdout)
        assert_equal(error_code, ErrorCode.AuthorizationError)
        assert_in('your app id', str(stdout))

def test_pdfprocess_sample_python(python3=False):
    set_python_path()
    args = ['../samples/python/pdfprocess.py', 'RenderPages', 'data/bad.pdf']
    if python3: args[0:0] = ['python3']
    with Stdout() as stdout:
        assert_equal(subprocess.call(args, stdout=stdout), 0)
        assert_in('your app id', str(stdout))

if platform.system() == 'Darwin':
    def test_pdfprocess_sample_python3():
        test_pdfprocess_sample_python(python3=True)
