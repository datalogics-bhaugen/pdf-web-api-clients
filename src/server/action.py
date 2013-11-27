"WebAPI action"

import os

from client import Client
from errors import APDFL_ERRORS, Error, ErrorCode, JSON, UNKNOWN


class Action(object):
    def __init__(self, request):
        self._client = Client(request.remote_addr, request.form)
        self._options = JSON.request_form_parser(request.form, 'options')
        self._request_form = request.form
        self._set_input(request)
    def raise_error(self, error):
        invalid_password = ErrorCode.InvalidPassword
        if error.code == invalid_password and not self.password:
            error.code = ErrorCode.MissingPassword
        raise error
    def _set_input(self, request, input_name=None):
        name = request.form.get('inputName', input_name or '<anon>')
        self._input_name = u'"{}"'.format(name) if u' ' in name else name
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
    def password(self): return self.request_form.get('password', None)
    @property
    def request_form(self): return self._request_form
