"WebAPI client"

import ThreeScalePY
import cfg

from ThreeScalePY import ThreeScaleAuthRep
from errors import Error, ErrorCode, HTTPCode, JSON, UNKNOWN


class Client(ThreeScaleAuthRep):
    def __init__(self, address, request_form):
        self._address = address
        form_parser = JSON.request_form_parser(request_form, 'application')
        app_id = form_parser.get('id', None)
        app_key = form_parser.get('key', None)
        provider_key = cfg.Configuration.three_scale.provider_key
        ThreeScaleAuthRep.__init__(self, provider_key, app_id, app_key)
    def authorize(self):
        try:
            if self.authrep(): return
            error = self.build_response().get_reason()
            if 'usage limit' in error.lower():
                limit_exceeded = ErrorCode.UsageLimitExceeded
                raise Error(limit_exceeded, error, HTTPCode.TooManyRequests)
        except ThreeScalePY.ThreeScaleException as exception:
            error = str(exception)
        authorization_error = ErrorCode.AuthorizationError
        raise Error(authorization_error, error, HTTPCode.Forbidden)
    @property
    def address(self): return self._address
    @property
    def application(self): return {'id': self.app_id, 'key': self.app_key}
