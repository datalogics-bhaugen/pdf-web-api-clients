"pdfprocess client"

import time
import ThreeScalePY
import simplejson as json
from ThreeScalePY import ThreeScaleAuthorize, ThreeScaleReport
from errors import Auth


PROVIDER_KEY = 'f362180da04b6ca1790784bde6ed70d6'


class Client(ThreeScaleAuthorize):
    def __init__(self, logger, request_form):
        self._logger = logger
        app_id, app_key = self._application(request_form)
        ThreeScaleAuthorize.__init__(self, PROVIDER_KEY, app_id, app_key)
        logger.info('request client: %s' % self)
        self._exc_info = None
    def __str__(self):
        return "(id='%s', key='%s')" % (self.app_id, self.app_key)
    def auth(self):
        try:
            if self.authorize(): return self._report()
            self._exc_info = self.build_auth_response().get_reason()
            return Auth.Invalid if 'invalid' in self.exc_info else Auth.TooFast
        except ThreeScalePY.ThreeScaleServerError:
            return Auth.Invalid
        except ThreeScalePY.ThreeScaleException as exc:
            self._logger.error(exc)
            return Auth.Unknown
    def _current_hits(self):
        reports = self.build_auth_response().get_usage_reports()
        hits = next((r for r in reports if r.get_metric() == 'hits'), None)
        if hits: return hits.get_current_value() # TODO: this is always 0!
    def _report(self):
        hits = self._current_hits()
        if hits:
            usage = {'hits': int(hits) + 1}
            transaction = {'app_id': self.app_id, 'usage': usage}
            report = ThreeScaleReport(PROVIDER_KEY, self.app_id, self.app_key)
            transaction.update({'timestamp': time.gmtime(time.time())})
            report.report([transaction])
        return Auth.OK
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

