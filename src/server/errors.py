"WebAPI error definitions"

import requests
import simplejson


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
    AdeptDRM = EnumValue('AdeptDRM', 6)
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
    def __init__(self, code, message, http_code=HTTPCode.BadRequest):
        Exception.__init__(self, message)
        self._code, self._http_code = code, http_code
    def __str__(self):
        return '{}: {}'.format(self.code, self.message)
    def copy(self, message=None):
        message = message or self.message
        return Error(self.code, message, self.http_code)
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
          'The file is damaged and could not be repaired'),
    Error(ErrorCode.InvalidPassword, 'This document requires authentication',
          HTTPCode.Forbidden),
    Error(ErrorCode.InvalidPassword,
          "The document's security settings do not permit this operation",
          HTTPCode.Forbidden),
    Error(ErrorCode.AdeptDRM,
          'The security plug-in required by this command is unavailable',
          HTTPCode.Forbidden)]

UNKNOWN = Error(ErrorCode.UnknownError, 'Internal server error',
                HTTPCode.InternalServerError)


class JSON:
    class RequestFormParser(dict):
        "support jQuery encoding of JSON form values"
        def parse(self, request_form, part_name):
            prefix = '{}['.format(part_name)
            for key, value in request_form.items():
                if key.startswith(prefix): self[key[len(prefix):-1]] = value
            self.update(JSON.parse(request_form.get(part_name, '{}')))
            return self
    @classmethod
    def parse(cls, json):
        try:
            return simplejson.loads(json)
        except Exception:
            error = 'cannot parse {}'.format(json)
            raise Error(ErrorCode.InvalidSyntax, error)
