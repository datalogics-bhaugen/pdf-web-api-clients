"pdfprocess action"

import ThreeScalePY
import flask

from ThreeScalePY import ThreeScaleAuthorize
from error import Auth, Error, ProcessCode, StatusCode


APP_ID = '2555417684482'
PROVIDER_KEY = 'f362180da04b6ca1790784bde6ed70d6'
TODO_BOGUS_API_KEY = 'f54ab5d8-5775-42c7-b888-f074ba892b57'


class AuthError(Error):
    def __init__(self, process_code, text, status_code=StatusCode.Forbidden):
        Error.__init__(self, process_code, text, status_code)

AUTH_ERRORS = [
    None,
    AuthError(ProcessCode.TooManyRequests, 'Usage limit exceeded',
        StatusCode.TooManyRequests),
    AuthError(ProcessCode.InvalidKey, 'Invalid API key'),
    AuthError(ProcessCode.InvalidPassword, 'Protected (invalid password)'),
    AuthError(ProcessCode.MissingPassword, 'Protected (missing password)'),
    AuthError(ProcessCode.AdeptDRM, 'Protected (ADEPT DRM)'),
    AuthError(ProcessCode.UnknownError, 'Unknown authorization error')]


class Action(object):
    def __init__(self, logger, request):
        self._api_key = request.form.get('apiKey', None)
        self._input = request.files['input']
        self._logger = logger
        self._request_form = request.form
    def abort(self, error):
        error_name = ProcessCode.format(error.process_code)
        self.logger.error('%s: %s' % (error_name, error.text))
        return self.response(error.process_code, error.text, error.status_code)
    def authorize(self):
        three_scale = ThreeScaleAuthorize(PROVIDER_KEY, APP_ID, self.api_key)
        try: return Auth.OK if three_scale.authorize() else Auth.TooFast
        except ThreeScalePY.ThreeScaleServerError:
            self.logger.warning('%s not authorized' % self.api_key)
            return Auth.OK # TODO: Auth.BadKey
        except ThreeScalePY.ThreeScaleException as exc:
            self.logger.error(exc)
            return Auth.Unknown
    def authorize_error(self, auth):
        return self.abort(AUTH_ERRORS[auth])
    @classmethod
    def response(cls, process_code, output, status_code=StatusCode.OK):
        json = flask.jsonify(processCode=process_code, output=output)
        return json, status_code
    @property
    def api_key(self): return self._api_key
    @property
    def input(self): return self._input
    @property
    def logger(self): return self._logger
    @property
    def request_form(self): return self._request_form

