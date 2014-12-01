"This module defines the classes and enumerations used to report errors."

import sys
import requests
import traceback

import cfg
import logger


class EnumValue(object):
    "Associates an error code (int) with its string representation."
    def __init__(self, name, value):
        self._name, self._value = name, value
    def __str__(self):
        return self._name
    def __int__(self):
        return self._value


class ErrorCode:
    "Error codes applicable to any request type:"
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
    "Associates an :py:class:`ErrorCode` with an :py:class:`HTTPCode`."
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
        "Return a copy of this error using the specified message."
        message = self._preferred_message or message or self.message
        return Error(self.code, message, self.http_code)
    def log(self):
        "Create a log entry for this error."
        logger.error(self)
        if self.code == ErrorCode.UnknownError:
            dlenv = cfg.Configuration.environment.dlenv
            for entry in traceback.format_tb(sys.exc_info()[2]):
                logger.error(entry.rstrip())
                if dlenv == 'prod' and '/eggs/' in entry: return
    @property
    def code(self):
        "The :py:class:`ErrorCode` for this error."
        return self._code
    @code.setter
    def code(self, value): self._code = value
    @property
    def http_code(self):
        "The :py:class:`HTTPCode` for this error."
        return self._http_code


INVALID_INPUT = "File does not begin with '%PDF-'."

USAGE_LIMIT = 'Your usage limit has been exceeded.' \
    ' Please contact us to increase your limit.'

ERRORS = [
    Error(ErrorCode.InvalidInput, INVALID_INPUT,
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

URL_ERROR = Error(ErrorCode.InvalidInput, INVALID_INPUT, HTTPCode.NotFound)

USAGE_LIMIT_ERROR =\
    Error(ErrorCode.UsageLimitExceeded, USAGE_LIMIT, HTTPCode.TooManyRequests)
