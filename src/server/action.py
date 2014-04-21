"WebAPI action"

import sys
import traceback

import cfg
import logger
from client import Client
from input import FromFile, FromURL
from errors import APDFL_ERRORS, Error, ErrorCode, HTTPCode, JSON, UNKNOWN


class Action(object):
    def __init__(self, request):
        self._client = Client(request.remote_addr, request.form)
        self._options = JSON.request_form_parser(request.form, 'options')
        self._request = request
        self._request_time = logger.iso8601_timestamp()
        self._input = FromURL(self) if self.input_url else FromFile(self)
    def __del__(self):
        del self._input
    def log_usage(self, error=None):
        usage = {'action': self.TYPE,
                 'address': self.client.address,
                 'client': self.client.application}
        if error:
            Action.log_error(error)
            error_code = int(error.code)
            usage['error'] = {'code': error_code, 'message': error.message}
        if self.input_name: usage['inputName'] = self.input_name
        if self.input_url: usage['inputURL'] = self.input_url
        if self.options: usage['options'] = self.options
        usage['password'] = True if self.password else False
        usage['requestTime'] = self._request_time
        usage['responseTime'] = logger.iso8601_timestamp()
        usage['status'] = error.http_code if error else HTTPCode.OK
        logger.info(JSON.dumps(usage))
    def raise_error(self, error):
        if error.code == ErrorCode.InvalidPassword and not self.password:
            error.code = ErrorCode.MissingPassword
        raise error
    @classmethod
    def get_error(cls, stdout):
        import pdf2img
        message = stdout.errors()
        for error_list in (APDFL_ERRORS, pdf2img.ERRORS):
            error = next((e for e in error_list if e.message in message), None)
            if error: return error.copy(message)
        return UNKNOWN.copy(message)
    @classmethod
    def log_error(cls, error):
        logger.error(error)
        if error.code == ErrorCode.UnknownError:
            dlenv = cfg.Configuration.environment.dlenv
            for entry in traceback.format_tb(sys.exc_info()[2]):
                logger.error(entry.rstrip())
                if dlenv == 'prod' and '/eggs/' in entry: return
    @property
    def client(self): return self._client
    @property
    def input(self): return self._input
    @property
    def input_name(self): return self.request.form.get('inputName', None)
    @property
    def input_url(self): return self.request.form.get('inputURL', None)
    @property
    def options(self): return self._options
    @property
    def password(self): return self.request.form.get('password', None)
    @property
    def request(self): return self._request
    @property
    def request_files(self): return self.request.files
