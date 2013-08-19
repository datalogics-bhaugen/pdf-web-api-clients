# TODO: instantiate pdfprocess.Client directly

"server regression tests, 3scale"

import uuid
import test
from test import Result, Test
from test_client import ProcessCode, StatusCode


RATE_LIMITED_ID = 'c953bc0d'
RATE_LIMITED_KEY = 'c7a7c21fb25c384127879ded5ed3b0a4'


def test_bad_application_id():
    bad_application_id = str(uuid.uuid4())[:8]
    _test_bad_application(bad_application_id, test.APPLICATION_KEY)

def test_bad_application_key():
    bad_application_key = str(uuid.uuid4()).replace('-', '')
    _test_bad_application(test.APPLICATION_ID, bad_application_key)

def _test_bad_application(application_id, application_key):
    result = Result(ProcessCode.AuthorizationError, StatusCode.Forbidden)
    bad_application = Test.pdf2img(application_id, application_key)
    Test(['data/bad.pdf'], result, bad_application).validate()

def TODO_usage_limit_exceeded():
    rate_limited_application = Test.pdf2img(RATE_LIMITED_ID, RATE_LIMITED_KEY)
    result = Result(ProcessCode.InvalidInput, StatusCode.BadRequest)
    for j in range(20): Test(['data/truncated.pdf'], result).validate()
    # TODO: ProcessCode.UsageLimitExceeded

