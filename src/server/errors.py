"WebAPI error definitions"

import requests
import simplejson

from cfg import Configuration


class EnumValue(object):
    def __init__(self, name, value):
        self._name, self._value = (name, value)
    def __str__(self):
        return self._name
    def __int__(self):
        return self._value


class ErrorCode(object):
    OK = EnumValue('OK', 0)
    AuthorizationError = EnumValue('AuthorizationError', 1)
    InvalidSyntax = EnumValue('InvalidSyntax', 2)
    InvalidInput = EnumValue('InvalidInput', 3)
    InvalidPassword = EnumValue('InvalidPassword', 4)
    MissingPassword = EnumValue('MissingPassword', 5)
    UnsupportedSecurityProtocol = EnumValue('UnsupportedSecurityProtocol', 6)
    InvalidOutputFormat = EnumValue('InvalidOutputFormat', 7)
    InvalidPage = EnumValue('InvalidPage', 8)
    RequestTooLarge = EnumValue('RequestTooLarge', 9)
    UsageLimitExceeded = EnumValue('UsageLimitExceeded', 10)
    UnknownError = EnumValue('UnknownError', 20)


class HTTPCode:
    OK = requests.codes.ok
    BadRequest = requests.codes.bad_request
    Forbidden = requests.codes.forbidden
    NotFound = requests.codes.not_found
    RequestEntityTooLarge = requests.codes.request_entity_too_large
    UnsupportedMediaType = requests.codes.unsupported_media_type
    TooManyRequests = requests.codes.too_many_requests
    InternalServerError = requests.codes.internal_server_error


class Error(Exception):
    def __init__(self, code, message, default_arg=None):
        Exception.__init__(self, message)
        self._code = code
        self._http_code, self._preferred_message = HTTPCode.BadRequest, None
        if type(default_arg) == int:
            self._http_code = default_arg
        else:
            self._preferred_message = default_arg
    def __str__(self):
        return u'{}: {}'.format(self.code, self.message)
    def copy(self, message=None):
        message = self._preferred_message or message or self.message
        return Error(self.code, message, self.http_code)
    @classmethod
    def validate_input_size(cls, input_size):
        max_input_size = int(Configuration.limits.input_size)
        if input_size > max_input_size:
            raise Error(ErrorCode.InvalidInput,
                        'input too large (max={})'.format(max_input_size),
                        HTTPCode.RequestEntityTooLarge)
    @property
    def code(self): return self._code
    @code.setter
    def code(self, value): self._code = value
    @property
    def http_code(self): return self._http_code


APDFL_ERRORS = [
    Error(ErrorCode.InvalidInput, "File does not begin with '%PDF-'",
          HTTPCode.UnsupportedMediaType),
    Error(ErrorCode.InvalidInput,
          'The file is damaged and could not be repaired',
          HTTPCode.UnsupportedMediaType),
    Error(ErrorCode.InvalidPassword, 'This document requires authentication',
          HTTPCode.Forbidden),
    Error(ErrorCode.InvalidPassword,
          "The document's security settings do not permit this operation",
          HTTPCode.Forbidden),
    Error(ErrorCode.UnsupportedSecurityProtocol,
          'The security plug-in required by this command is unavailable',
          HTTPCode.Forbidden)]

UNKNOWN = Error(ErrorCode.UnknownError, 'Internal server error',
                HTTPCode.InternalServerError)


class JSON:
    class RequestFormParser(dict):
        "support jQuery encoding of JSON form values"
        def parse(self, request_form, part_name):
            prefix = u'{}['.format(part_name)
            for key, value in request_form.items():
                if key.startswith(prefix): self[key[len(prefix):-1]] = value
            self.update(JSON.loads(request_form.get(part_name, u'{}')))
    @classmethod
    def request_form_parser(cls, request_form, part_name):
        result = JSON.RequestFormParser()
        result.parse(request_form, part_name)
        return result
    @classmethod
    def dumps(cls, obj):
        try:
            return simplejson.dumps(obj, sort_keys=True)
        except Exception:
            error = u'cannot encode {}'.format(obj)
            raise Error(ErrorCode.InvalidSyntax, error)
    @classmethod
    def loads(cls, s):
        try:
            return simplejson.loads(s)
        except Exception:
            error = u'cannot parse {}'.format(s)
            raise Error(ErrorCode.InvalidSyntax, error)
