"pdfprocess action"

import ThreeScalePY
import flask
import simplejson as json

from ThreeScalePY import ThreeScaleAuthorize
from errors import Auth, Error, ProcessCode, StatusCode


PROVIDER_KEY = 'f362180da04b6ca1790784bde6ed70d6'


AUTH_ERRORS = [
    None,
    Error(ProcessCode.UsageLimitExceeded, 'Usage limit exceeded',
        StatusCode.TooManyRequests),
    Error(ProcessCode.AuthorizationError, '3scale', StatusCode.Forbidden),
    None]


class Client(object):
    def __init__(self, request_application):
        application = json.loads(request_application)
        self._id = str(application.get('id', ''))
        self._key = str(application.get('key', ''))
    def __str__(self):
        return "(id='%s', key='%s')" % (self._id, self._key)
    def authorize(self):
        three_scale = ThreeScaleAuthorize(PROVIDER_KEY, self._id, self._key)
        return three_scale.authorize()


class Action(object):
    def __init__(self, logger, request):
        self._client = Client(request.form.get('application', '{}'))
        self._input = request.files['input']
        self._logger = logger
        self._request_form = request.form
    def abort(self, error):
        self.logger.error(error)
        process_code = int(error.process_code)
        return self.response(process_code, error.text, error.status_code)
    def authorize(self):
        try:
            if self.client.authorize(): return Auth.OK
        except ThreeScalePY.ThreeScaleServerError:
            return self._not_authorized()
        except ThreeScalePY.ThreeScaleException as exc:
            self.logger.error(exc)
            return Auth.Unknown
        return self._not_authorized() # TODO: Auth.TooFast when appropriate
    def authorize_error(self, auth):
        return self.abort(AUTH_ERRORS[auth])
    def _not_authorized(self):
        self.logger.error('%s not authorized' % self.client)
        return Auth.NotAuthorized
    @classmethod
    def response(cls, process_code, output, status_code=StatusCode.OK):
        json = flask.jsonify(processCode=int(process_code), output=output)
        return json, status_code
    @property
    def client(self): return self._client
    @property
    def input(self): return self._input
    @property
    def logger(self): return self._logger
    @property
    def request_form(self): return self._request_form

