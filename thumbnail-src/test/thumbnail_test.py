"thumbnail regression tests"

import test
from nose.tools import assert_true

def test_form_data_url(): assert_true(test.run(data=test.INPUT))
def test_query_string_url(): assert_true(test.run(params=test.INPUT))
