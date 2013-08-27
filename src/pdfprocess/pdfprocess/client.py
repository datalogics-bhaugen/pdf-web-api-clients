"pdfprocess client"

import time
import ThreeScalePY
import simplejson as json
from ThreeScalePY import ThreeScaleAuthRep, ThreeScaleReport
from errors import Auth


PROVIDER_KEY = 'f362180da04b6ca1790784bde6ed70d6'


class Client(ThreeScaleAuthRep):
    def __init__(self, logger, request_form):
        self._logger = logger
        app_id, app_key = self._application(request_form)
        ThreeScaleAuthRep.__init__(self, PROVIDER_KEY, app_id, app_key)
        logger.info('request client: %s' % self)
        self._exc_info = None
    def __str__(self):
        return "(id='%s', key='%s')" % (self.app_id, self.app_key)
    def auth(self):
        try:
            if self.authrep(): return Auth.OK
            self._exc_info = self.build_response().get_reason()
            if 'usage limit' in self.exc_info: return Auth.TooFast
            return Auth.Invalid
        except ThreeScalePY.ThreeScaleException as exc:
            self._logger.error(exc)
            return Auth.Unknown
    def _application(self, request_form):
        application = request_form.get('application', None)
        if isinstance(application, unicode) or isinstance(application, str):
            application = json.loads(application)
        if application:
            app_id = application.get('id', '')
            app_key = application.get('key', '')
        else:
            app_id = request_form.get('application[id]', '')
            app_key = request_form.get('application[key]', '')
        return app_id, app_key
    @property
    def exc_info(self): return self._exc_info

