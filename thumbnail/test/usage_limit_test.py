"usage limit initialization test"

import test
from server.usage_limit import DEFAULT_RATE_LIMITS, PlanLimit
from nose.tools import assert_equal

def test_initialization():
    rate_limits = [str(rate_limit) for rate_limit in PlanLimit().rate_limits]
    default_limits = [str(rate_limit) for rate_limit in DEFAULT_RATE_LIMITS]
    assert_equal(sorted(rate_limits), sorted(default_limits))
