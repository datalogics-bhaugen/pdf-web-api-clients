"pdfprocess action"

import ThreeScalePY
import flask
import simplejson as json

from ThreeScalePY import ThreeScaleAuthorize
from client import Client
from errors import APDFL_ERRORS, Error, ProcessCode, StatusCode, UNKNOWN


PROVIDER_KEY = 'f362180da04b6ca1790784bde6ed70d6'


AUTH_ERRORS = [
    None,
    Error(ProcessCode.UsageLimitExceeded, None, StatusCode.TooManyRequests),
    Error(ProcessCode.AuthorizationError, None, StatusCode.Forbidden),
    None]


class Action(object):
    def __init__(self, logger, request):
        self._client = Client(logger, request.form)
        request_files = request.files.values()
        self._input = request_files[0] if request_files else None
        self._logger = logger
        self._options = json.loads(request.form.get('options', '{}'))
        self._request_form = request.form
    def abort(self, error):
        no_password = not self._password_received()
        if error.process_code == ProcessCode.InvalidPassword and no_password:
            error.process_code = ProcessCode.MissingPassword
        self.logger.error(error)
        return \
            self.response(error.process_code, error.message, error.status_code)
    def authorize(self):
        return self.client.auth()
    def authorize_error(self, auth):
        return self.abort(AUTH_ERRORS[auth].copy(self.client.exc_info))
    def get_error(self):
        import image
        for errors in (APDFL_ERRORS, image.ERRORS):
            error =\
                next((e for e in errors if e.message in self.exc_info), None)
            if error: return error.copy(self.exc_info)
        return UNKNOWN.copy(self.exc_info)
    def _password_received(self):
        for key in self.options.keys():
            if key.lower() == 'password': return True
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
    def options(self): return self._options
    @property
    def request_form(self): return self._request_form

