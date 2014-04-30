"thumbnail regression tests"

import test
from nose.tools import assert_equal, assert_true

def test_form_data_url(): assert_true(test.run(data=test.INPUT).ok)
def test_query_string_url(): assert_true(test.run(params=test.INPUT).ok)

def test_bad_url():
    response = test.run(data=test.BAD_INPUT)
    assert_equal(response.error_code, 3)  # InvalidInput
    assert_equal(response.http_code, 415)  # UnsupportedMediaType
