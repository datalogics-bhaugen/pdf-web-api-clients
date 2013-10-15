"pdfprocess action"

import os

from client import Client
from errors import APDFL_ERRORS, Error, JSON, ProcessCode, StatusCode, UNKNOWN


AUTH_ERRORS = [
    None,  # Auth.OK
    Error(ProcessCode.UsageLimitExceeded, None, StatusCode.TooManyRequests),
    Error(ProcessCode.AuthorizationError, None, StatusCode.Forbidden)]


class Action(object):
    def __init__(self, request):
        self._client = Client(request.remote_addr, request.form)
        self._options = JSON.parse(request.form.get('options', '{}'))
        self._request_form = request.form
        self._set_input(request)
    def authorize(self):
        return self.client.auth()
    def raise_authorize_error(self, auth):
        self.raise_error(AUTH_ERRORS[auth].copy(self.client.exc_info))
    def raise_error(self, error):
        no_password = not self._password_received()
        if error.process_code == ProcessCode.InvalidPassword and no_password:
            error.process_code = ProcessCode.MissingPassword
        raise error
    def _password_received(self):
        for key in self.options.keys():
            if key.lower() == 'password': return True
    def _set_input(self, request, input_name=None):
        name = request.form.get('inputName', input_name or '<anon>')
        self._input_name = '"%s"' % name if ' ' in name else name
    @classmethod
    def get_error(cls, stdout):
        import pdf2img
        errors = stdout.errors()
        for error_list in (APDFL_ERRORS, pdf2img.ERRORS):
            error = next((e for e in error_list if e.message in errors), None)
            if error: return error.copy(errors)
        return UNKNOWN.copy(errors)
    @property
    def client(self): return self._client
    @property
    def input(self): return self._input
    @property
    def input_name(self): return self._input_name
    @property
    def options(self): return self._options
    @property
    def request_form(self): return self._request_form
