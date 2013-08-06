"server regression tests"

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

