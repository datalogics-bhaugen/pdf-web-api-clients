"This module encapsulates our 3scale dependency."

import ThreeScalePY
import cfg
import logger
import time

from ThreeScalePY import ThreeScaleAuthRep
from errors import Error, ErrorCode, HTTPCode
from request import JSON


USAGE_LIMIT = 'Your usage limit has been exceeded. ' \
    'Please contact us to increase your limit.'

class Client(ThreeScaleAuthRep):
    "Extract application ID/key from request and authenticate it."
    def __init__(self, address, request_form):
        self._address = address
        request_data = JSON.request_data(request_form, 'application')
        app_id = request_data.get('id', None)
        app_key = request_data.get('key', None)
        provider_key = cfg.Configuration.three_scale.provider_key
        ThreeScaleAuthRep.__init__(self, provider_key, app_id, app_key)
    def authenticate(self):
        "Use 3scale API to authenticate client."
        error, max_retries = None, int(cfg.Configuration.authrep.max_retries)
        for retry in range(max_retries + 1):
            error = self._authrep_error()
            if error is None: return
            if retry < max_retries:
                time.sleep(int(cfg.Configuration.authrep.retry_delay))
        raise Error(ErrorCode.AuthorizationError, error, HTTPCode.Forbidden)
    def _authrep_error(self):
        try:
            if self.authrep(): return None
            error_code = ErrorCode.AuthorizationError
            error = self.build_response().get_reason()
            if 'usage limit' in error.lower():
                # TODO: do something to address repeated violations?
                error_code = ErrorCode.UsageLimitExceeded
                raise Error(error_code, USAGE_LIMIT, HTTPCode.TooManyRequests)
            raise Error(error_code, error, HTTPCode.Forbidden)
        except ThreeScalePY.ThreeScaleException as exception:
            error = str(exception)
            logger.error(error)
            return error
        pass  # not reachable
    @property
    def address(self):
        "The IP address for this client."
        return self._address
    @property
    def application(self):
        "The 3scale credentials for this client."
        return {'id': self.app_id, 'key': self.app_key}
