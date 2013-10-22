"WebAPI pdf2img action errors"

import server
from server import EnumValue, Error, HTTPCode


class ErrorCode(server.ErrorCode):
    InvalidColorModel = EnumValue('InvalidColorModel', 31)
    InvalidCompression = EnumValue('InvalidCompression', 32)
    InvalidRegion = EnumValue('InvalidRegion', 33)
    InvalidResolution = EnumValue('InvalidResolution', 34)


ERRORS = [
    Error(ErrorCode.InvalidOutputFormat, 'Invalid output type'),
    Error(ErrorCode.InvalidPage, "Bad '-pages' argument"),
    Error(ErrorCode.InvalidPage, "Could not parse '-pages' option"),
    Error(ErrorCode.InvalidPage, 'is greater than End page'),
    Error(ErrorCode.InvalidPage, 'is greater than last PDF page'),
    Error(ErrorCode.InvalidPage, 'last PDF page is'),
    Error(ErrorCode.RequestTooLarge, 'Insufficient memory available',
          HTTPCode.RequestEntityTooLarge),
    Error(ErrorCode.RequestTooLarge, 'pdf2img ran out of memory',
          HTTPCode.RequestEntityTooLarge),
    Error(ErrorCode.InvalidColorModel, 'Invalid color model'),
    Error(ErrorCode.InvalidColorModel,
          'GIF only supports RGB and Gray images'),
    Error(ErrorCode.InvalidCompression, 'Invalid compression type'),
    Error(ErrorCode.InvalidRegion, 'Invalid PDF region type'),
    Error(ErrorCode.InvalidResolution, "'-resolution' bad value specified")]
