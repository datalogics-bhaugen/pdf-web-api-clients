"server environment tests"

import test
from test_client import ProcessCode as ProcessCode, StatusCode

BASE_URL = 'https://pdfprocess%s.datalogics-cloud.com'
PROD_URL, TEST_URL = (BASE_URL % '', BASE_URL % '-test')

ok_result = test.Result(ProcessCode.OK, StatusCode.OK)
monitor = test.Test(['data/four_pages.pdf'], ok_result)

def prod_environment_test(): monitor(test.VERSION, PROD_URL)
def test_environment_test(): monitor(test.VERSION, TEST_URL)
