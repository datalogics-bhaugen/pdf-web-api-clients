"pdfprocess action"

import ThreeScalePY
import flask

from ThreeScalePY import ThreeScaleAuthorize
from client import Client
from errors import APDFL_ERRORS, Error, JSON, ProcessCode, StatusCode, UNKNOWN


PROVIDER_KEY = 'f362180da04b6ca1790784bde6ed70d6'


AUTH_ERRORS = [
    None, # Auth.OK
    Error(ProcessCode.UsageLimitExceeded, None, StatusCode.TooManyRequests),
    Error(ProcessCode.AuthorizationError, None, StatusCode.Forbidden)]


class Action(object):
    def __init__(self, logger, request):
        self._client = Client(logger, request.form)
        self._input = Action.request_input(request)
        self._options = JSON.parse(request.form.get('options', '{}'))
        self._request_form = request.form
        self._logger = logger
    def authorize(self):
        return self.client.auth()
    def authorize_error(self, auth):
        self.raise_error(AUTH_ERRORS[auth].copy(self.client.exc_info))
    def raise_error(self, error):
        no_password = not self._password_received()
        if error.process_code == ProcessCode.InvalidPassword and no_password:
            error.process_code = ProcessCode.MissingPassword
        raise error
    def _password_received(self):
        for key in self.options.keys():
            if key.lower() == 'password': return True
    @classmethod
    def get_error(cls, stdout):
        import image
        stdout_errors = stdout.errors()
        for errors in (APDFL_ERRORS, image.ERRORS):
            error =\
                next((e for e in errors if e.message in stdout_errors), None)
            if error: return error.copy(stdout_errors)
        return UNKNOWN.copy(stdout_errors)
    @classmethod
    def request_input(cls, request):
        request_files = request.files.values()
        invalid_input = ProcessCode.InvalidInput
        if not request_files: raise Error(invalid_input, 'no input')
        if len(request_files) > 1: raise Error(invalid_input, 'excess input')
        return request_files[0]
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

