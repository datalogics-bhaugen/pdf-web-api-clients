"thumbnail regression tests"

import subprocess
from tmpdir import Stdout
from nose.tools import assert_equal

def test_thumbnail():
    thumbnail_url = '127.0.0.1:5050'
    input_url = 'inputURL=%s' % 'http://www.datalogics.com/pdf/doc/pdf2img.pdf'
    input = ['curl', '--request', 'GET', '--form', input_url, thumbnail_url]
    assert_equal(subprocess.call(input, stdout=Stdout(), stderr=Stdout()), 0)
