import abc
import sys
import traceback

import cfg
import input
import logger
from client import Client
from errors import APDFL_ERRORS, Error, ErrorCode, HTTPCode, UNKNOWN
from request import JSON


class Action(object):
    "Each request handler should inherit from this class."
    __metaclass__ = abc.ABCMeta
    def __init__(self, request):
        self._client = Client(request.remote_addr, request.form)
        self._options = JSON.request_data(request.form, 'options')
        self._request = request
        self._request_time = logger.iso8601_timestamp()
        self._input = input.Input.make(self)
    @abc.abstractmethod
    def __call__(self):
        pass
    def __del__(self):
        self._input = None
    def log_usage(self, error=None):
        "Create a log entry for this request."
        usage = {'action': self.request_type,
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
        usage['serverVersion'] = cfg.Configuration.versions.server_tag
        logger.info(JSON.dumps(usage))
    def raise_error(self, error):
        "Raise an exception for this request."
        if error.code == ErrorCode.InvalidPassword and not self.password:
            error.code = ErrorCode.MissingPassword
        raise error
    @classmethod
    def get_error(cls, stdout):
        "Parse *stdout* to create appropriate :py:class:`~.Error`."
        import pdf2img
        message = stdout.errors()
        for error_list in (APDFL_ERRORS, pdf2img.ERRORS):
            error = next((e for e in error_list if e.message in message), None)
            if error: return error.copy(message)
        return UNKNOWN.copy(message)
    @classmethod
    def log_error(cls, error):
        "Create a log entry for an :py:class:`~.Error`."
        logger.error(error)
        if error.code == ErrorCode.UnknownError:
            dlenv = cfg.Configuration.environment.dlenv
            for entry in traceback.format_tb(sys.exc_info()[2]):
                logger.error(entry.rstrip())
                if dlenv == 'prod' and '/eggs/' in entry: return
    @abc.abstractproperty
    def request_type(self):
        "*(abstract)* The request's type, e.g. RenderPages."
        return None
    @property
    def client(self):
        "The :py:class:`~.Client` for this request."
        return self._client
    @property
    def input(self):
        "The :py:class:`~.Input` for this request."
        return self._input
    @property
    def input_name(self):
        "The client's *inputName* for this request."
        return self.request.form.get('inputName', None)
    @property
    def input_url(self):
        "The URL for this request's :py:class:`~.Input`."
        return self.request.form.get('inputURL', None)
    @property
    def options(self):
        "The options (dict) for this request."
        return self._options
    @property
    def password(self):
        "The password for this request's :py:class:`~.Input`."
        return self.request.form.get('password', None)
    @property
    def request(self):
        "The raw (Flask) request."
        return self._request
    @property
    def request_files(self):
        "The files for this request."
        return self.request.files
