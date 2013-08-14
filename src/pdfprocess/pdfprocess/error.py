"pdfprocess error classes"


class Auth:
    "for internal use only"
    OK, TooFast, BadKey, BadPassword, NoPassword, DRM, Unknown = range(7)


class Code(object):
    @classmethod
    def format(cls, code):
        return next(kv for kv in cls.__dict__.iteritems() if kv[1] == code)[0]

class ProcessCode(Code):
    OK = 0
    InvalidKey = 1
    InvalidSyntax = 2
    InvalidInput = 3
    InvalidPassword = 4
    MissingPassword = 5
    AdeptDRM = 6
    InvalidOutputType = 7
    InvalidPage = 8
    RequestTooLarge = 9
    TooManyRequests = 10
    UnknownError = 20

class ImageProcessCode(ProcessCode):
    InvalidColorSpace = 21
    InvalidCompression = 22
    InvalidRegion = 23

class StatusCode(Code):
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
    @property
    def process_code(self): return self._process_code
    @property
    def status_code(self): return self._status_code
    @property
    def text(self): return self._text
    @process_code.setter
    def process_code(self, value): self._process_code = value

