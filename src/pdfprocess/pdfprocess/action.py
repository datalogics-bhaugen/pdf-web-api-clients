"pdfprocess action"

import ThreeScalePY
import flask

from ThreeScalePY import ThreeScaleAuthorize


APP_ID = '2555417684482'
PROVIDER_KEY = 'f362180da04b6ca1790784bde6ed70d6'
TODO_BOGUS_API_KEY = 'f54ab5d8-5775-42c7-b888-f074ba892b57'


class Auth:
    Ok, TooFast, BadKey, BadPassword, NoPassword, DRM, Unknown = range(7)


class Action(object):
    def __init__(self, logger, request):
        self._input = request.files['input']
        self._logger = logger
        self._request_form = request.form
    def abort(self, process_code, text, status_code=500):
        self.logger.error('%s: %s' % (process_code, text))
        return self.response(status_code, process_code, text)
    def authorize(self):
        api_key = self.request_form.get('apiKey', None)
        if api_key == TODO_BOGUS_API_KEY: return Auth.Ok
        three_scale = ThreeScaleAuthorize(PROVIDER_KEY, APP_ID, api_key)
        try: return Auth.Ok if three_scale.authorize() else Auth.TooFast
        except ThreeScalePY.ThreeScaleServerError:
            return Auth.BadKey
        except ThreeScalePY.ThreeScaleException as exc:
            self.logger.error(exc)
            return Auth.Unknown
    def authorize_error(self, auth):
        # TODO: process codes
        if auth == Auth.TooFast:
            return self.abort(1013, 'Usage limit exceeded', 403)
        if auth == Auth.BadKey:
            return self.abort(1013, 'Invalid API key', 403)
        if auth == Auth.DRM:
            return self.abort(1013, 'Protected (ADEPT DRM)', 403)
        if auth == Auth.BadPassword:
            return self.abort(1013, 'Protected (invalid password)', 403)
        if auth == Auth.NoPassword:
            return self.abort(1013, 'Protected (no password)', 403)
    @classmethod
    def response(cls, status_code, process_code, output):
        json = flask.jsonify(processCode=process_code, output=output)
        return json, status_code
    @property
    def input(self): return self._input
    @property
    def logger(self): return self._logger
    @property
    def request_form(self): return self._request_form

