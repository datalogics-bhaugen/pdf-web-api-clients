"pdfprocess action"

import ThreeScalePY
import flask
import simplejson as json

from ThreeScalePY import ThreeScaleAuthorize
from error import Auth, Error, ProcessCode, StatusCode


PROVIDER_KEY = 'f362180da04b6ca1790784bde6ed70d6'


ERRORS = [
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
        return "{id:'%s', key:'%s'}" % (self.id, self.key)
    def authorize(self):
        return ThreeScaleAuthorize(PROVIDER_KEY, self.id, self.key).authorize()
    @property
    def id(self): return self._id
    @property
    def key(self): return self._key


class Action(object):
    def __init__(self, logger, request):
        self._client = Client(request.form.get('application', '{}'))
        self._input = request.files['input']
        self._logger = logger
        self._request_form = request.form
    def abort(self, error):
        self.logger.error(error)
        return self.response(error.process_code, error.text, error.status_code)
    def authorize(self):
        try: return Auth.OK if self.client.authorize() else Auth.TooFast
        except ThreeScalePY.ThreeScaleServerError:
            self.logger.error('%s not authorized' % self.client)
            return Auth.NotAuthorized
        except ThreeScalePY.ThreeScaleException as exc:
            self.logger.error(exc)
            return Auth.Unknown
    def authorize_error(self, auth):
        return self.abort(ERRORS[auth])
    @classmethod
    def response(cls, process_code, output, status_code=StatusCode.OK):
        json = flask.jsonify(processCode=process_code, output=output)
        return json, status_code
    @property
    def client(self): return self._client
    @property
    def input(self): return self._input
    @property
    def logger(self): return self._logger
    @property
    def request_form(self): return self._request_form

