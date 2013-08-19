"pdfprocess error classes"


class Auth:
    "for internal use only"
    OK, TooFast, NotAuthorized, Unknown = range(4)


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


class Error(object):
    def __init__(self, process_code, text, status_code=StatusCode.BadRequest):
        self._process_code = process_code
        self._status_code = status_code
        self._text = text
    def __str__(self):
        return '%s: %s' % (self.process_code, self.text)
    @property
    def process_code(self): return self._process_code
    @property
    def status_code(self): return self._status_code
    @property
    def text(self): return self._text
    @process_code.setter
    def process_code(self, value): self._process_code = value

