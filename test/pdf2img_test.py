"pdf2img resource regression tests"

import os
import glob
import platform
import subprocess
from server.tmpdir import Stdout
from nose.tools import assert_equal, assert_in


def test_pdf2img_application():
    assert_in('PDF2IMG', call(['pdf2img', 'data/hello_world.pdf', 'tif']))

def call(args):
    with Stdout() as stdout:
        assert_equal(subprocess.call(args, stdout=stdout), 0)
        return str(stdout)

if platform.system() == 'Linux':
    def test_pdf2img_resources():
        resource_dir = os.path.join(os.sep + 'opt', 'pdfprocess', 'Resource')
        for font_list in glob.glob(os.path.join(resource_dir, 'AdobeFnt*')):
            args = ['grep', '-c', 'FamilyName:Verdana', font_list]
            assert_equal('4', call(args).rstrip())
