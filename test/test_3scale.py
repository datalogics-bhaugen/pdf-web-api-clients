"server regression tests, 3scale"

import uuid
import test
from test import Result, Test
from test_client import ProcessCode, StatusCode


def test_bad_application_id():
    bad_application_id = str(uuid.uuid4())[:8]
    bad_application = Test.pdf2img(bad_application_id, test.APPLICATION_KEY)
    result = Result(ProcessCode.AuthorizationError, StatusCode.Forbidden)
    Test(['data/bad.pdf', 'jpg'], result, bad_application).validate()

def test_bad_application_key():
    bad_application_key = str(uuid.uuid4()).replace('-', '')
    bad_application = Test.pdf2img(test.APPLICATION_ID, bad_application_key)
    result = Result(ProcessCode.AuthorizationError, StatusCode.Forbidden)
    Test(['data/bad.pdf', 'jpg'], result, bad_application).validate()

