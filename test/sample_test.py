"sample regression tests"

import os
import glob
import subprocess
from pdfprocess.stdout import Stdout
from nose.tools import assert_equal, assert_in


def set_python_path():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    eggs_dir = os.path.join(root_dir, 'eggs')
    json_dir = glob.glob(os.path.join(eggs_dir, 'simplejson-*.egg'))[0]
    requests_dir = glob.glob(os.path.join(eggs_dir, 'requests-*.egg'))[0]
    os.environ['PYTHONPATH'] = '%s:%s' % (json_dir, requests_dir)

def test_pdf2img():
    set_python_path()
    args = ['python', '../samples/python/pdf2img.py', 'data/bad.pdf']
    with Stdout() as stdout:
        assert_equal(subprocess.call(args, stdout=stdout), 0)
        assert_in('TODO: Application ID', str(stdout))

