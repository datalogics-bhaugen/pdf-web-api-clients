"web_api client"

import ThreeScalePY
import logger

from ThreeScalePY import ThreeScaleAuthRep
from errors import Error, JSON, ProcessCode, StatusCode, UNKNOWN


PROVIDER_KEY = 'f362180da04b6ca1790784bde6ed70d6'


class Client(ThreeScaleAuthRep):
    def __init__(self, address, request_form):
        app_id, app_key = self._application(request_form)
        logger.info("{}: id='{}', key='{}'".format(address, app_id, app_key))
        ThreeScaleAuthRep.__init__(self, PROVIDER_KEY, app_id, app_key)
    def __str__(self):
        return "(id='{}', key='*{}')".format(self.app_id, self.app_key[-7:])
    def authorize(self):
        try:
            if self.authrep(): return
            error = self.build_response().get_reason()
            if 'usage limit' in error.lower():
                limit_exceeded = ProcessCode.UsageLimitExceeded
                raise Error(limit_exceeded, error, StatusCode.TooManyRequests)
        except ThreeScalePY.ThreeScaleException as exception:
            error = str(exception)
        authorization_error = ProcessCode.AuthorizationError
        raise Error(authorization_error, error, StatusCode.Forbidden)
    def _application(self, request_form):
        application = self._decode_application(request_form)
        if application:
            app_id = application.get('id', '')
            app_key = application.get('key', '')
        else:
            app_id = request_form.get('application[id]', '')
            app_key = request_form.get('application[key]', '')
        return app_id, app_key
    def _decode_application(self, request_form):
        app = request_form.get('application', None)
        return JSON.parse(app) if type(app) in (str, unicode) else app
