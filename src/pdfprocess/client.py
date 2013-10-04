"pdfprocess client"

import ThreeScalePY
from ThreeScalePY import ThreeScaleAuthRep
from errors import Auth, JSON


PROVIDER_KEY = 'f362180da04b6ca1790784bde6ed70d6'


class Client(ThreeScaleAuthRep):
    def __init__(self, logger, address, request_form):
        self._logger = logger
        app_id, app_key = self._application(request_form)
        logger.info("%s: id='%s', key='%s'" % (address, app_id, app_key))
        ThreeScaleAuthRep.__init__(self, PROVIDER_KEY, app_id, app_key)
        self._exc_info = None
    def __str__(self):
        return "(id='%s', key='*%s')" % (self.app_id, self.app_key[-7:])
    def auth(self):
        try:
            if self.authrep(): return Auth.OK
            self._exc_info = self.build_response().get_reason()
            usage_limit = 'usage limit' in self.exc_info
            return Auth.UsageLimitExceeded if usage_limit else Auth.Invalid
        except ThreeScalePY.ThreeScaleException as exc:
            self._logger.error(exc)
            return Auth.Invalid
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
        is_string = isinstance(app, unicode) or isinstance(app, str)
        return JSON.parse(app) if is_string else app
    @property
    def exc_info(self): return self._exc_info
