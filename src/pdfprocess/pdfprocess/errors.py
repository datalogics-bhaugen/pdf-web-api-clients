"pdfprocess error definitions"

import simplejson


class Auth:
    "for internal use only"
    OK, UsageLimitExceeded, Invalid, Unknown = range(4)


class EnumValue(object):
    def __init__(self, name, value):
        self._name, self._value = (name, value)
    def __str__(self):
        return self._name
    def __int__(self):
        return self._value


class ProcessCode(object):
    OK = EnumValue('OK', 0)
    AuthorizationError = EnumValue('AuthorizationError', 1)
    InvalidSyntax = EnumValue('InvalidSyntax', 2)
    InvalidInput = EnumValue('InvalidInput', 3)
    InvalidPassword = EnumValue('InvalidPassword', 4)
    MissingPassword = EnumValue('MissingPassword', 5)
    AdeptDRM = EnumValue('AdeptDRM', 6)
    InvalidOutputType = EnumValue('InvalidOutputType', 7)
    InvalidPage = EnumValue('InvalidPage', 8)
    RequestTooLarge = EnumValue('RequestTooLarge', 9)
    UsageLimitExceeded = EnumValue('UsageLimitExceeded', 10)
    UnknownError = EnumValue('UnknownError', 20)


class StatusCode:
    OK = 200
    BadRequest = 400
    Forbidden = 403
    NotFound = 404
    RequestEntityTooLarge = 413
    UnsupportedMediaType = 415
    TooManyRequests = 429
    InternalServerError = 500


class Error(Exception):
    def __init__(self, process_code, message,
      status_code=StatusCode.BadRequest):
        Exception.__init__(self, message)
        self._process_code = process_code
        self._status_code = status_code
    def __repr__(self):
        return '%s: %s' % (self.process_code, self.message)
    def copy(self, message=None):
        message = message or self.message
        return Error(self.process_code, message, self.status_code)
    @property
    def process_code(self): return self._process_code
    @property
    def status_code(self): return self._status_code
    @process_code.setter
    def process_code(self, value): self._process_code = value


APDFL_ERRORS = [
    Error(ProcessCode.InvalidInput, "File does not begin with '%PDF-'",
        StatusCode.UnsupportedMediaType),
    Error(ProcessCode.InvalidInput,
        'The file is damaged and could not be repaired'),
    Error(ProcessCode.InvalidPassword, 'This document requires authentication',
        StatusCode.Forbidden),
    Error(ProcessCode.AdeptDRM,
        'The security plug-in required by this command is unavailable',
        StatusCode.Forbidden)]

UNKNOWN = Error(ProcessCode.UnknownError, 'Internal server error',
    StatusCode.InternalServerError)


class JSON(object):
    def __init__(self, logger):
        self._logger = logger
    def parse(self, s):
        try:
            return simplejson.loads(s)
        except Exception: 
            error = Error(ProcessCode.InvalidSyntax, 'cannot parse %s' % s)
            self._logger.error(error.message)
            raise error

