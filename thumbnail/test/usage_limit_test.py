"usage limits initialization test"

import test
from server.usage_limit import DEFAULT_USAGE_LIMITS, PlanLimit
from nose.tools import assert_equal, assert_in

def test_initialization():
    usage_limits = PlanLimit().usage_limits
    default_usage_limits = [str(limit) for limit in DEFAULT_USAGE_LIMITS]
    assert_equal(len(usage_limits), len(default_usage_limits))
    for usage_limit in usage_limits:
        assert_in(str(usage_limit), default_usage_limits)
