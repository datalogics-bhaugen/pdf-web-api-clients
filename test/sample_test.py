"web_api regression tests"

import os
import glob
import platform
import subprocess
from web_api.tmpdir import Stdout
from test_client import ProcessCode
from nose.tools import assert_equal, assert_in


def set_python_path():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    eggs_dir = os.path.join(root_dir, 'eggs')
    json_dir = glob.glob(os.path.join(eggs_dir, 'simplejson-*.egg'))[0]
    requests_dir = glob.glob(os.path.join(eggs_dir, 'requests-*.egg'))[0]
    os.environ['PYTHONPATH'] = '{}:{}'.format(json_dir, requests_dir)

def test_pdf2img_application():
    args = ['pdf2img', 'data/hello_world.pdf', 'tif']
    with Stdout() as stdout:
        assert_equal(subprocess.call(args, stdout=stdout), 0)
        assert_in('PDF2IMG', str(stdout))

def test_pdfprocess_sample_perl():
    args = ['../samples/perl/pdfprocess.pl', 'render/pages', 'data/bad.pdf']
    with Stdout() as stdout:
        process_code = subprocess.call(args, stdout=stdout)
        assert_equal(process_code, ProcessCode.AuthorizationError)
        assert_in('TODO: Application ID', str(stdout))

def test_pdfprocess_sample_python(python3=False):
    set_python_path()
    args = ['../samples/python/pdfprocess.py', 'render/pages', 'data/bad.pdf']
    if python3: args[0:0] = ['python3']
    with Stdout() as stdout:
        assert_equal(subprocess.call(args, stdout=stdout), 0)
        assert_in('TODO: Application ID', str(stdout))

if platform.system() == 'Darwin':
    def test_pdfprocess_sample_python3():
        test_pdfprocess_sample_python(python3=True)
