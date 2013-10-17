"web_api pdf2img action errors"

import web_api
from web_api import EnumValue, Error, StatusCode


class ProcessCode(web_api.ProcessCode):
    InvalidColorModel = EnumValue('InvalidColorModel', 31)
    InvalidCompression = EnumValue('InvalidCompression', 32)
    InvalidRegion = EnumValue('InvalidRegion', 33)
    InvalidResolution = EnumValue('InvalidResolution', 34)


ERRORS = [
    Error(ProcessCode.InvalidOutputFormat, 'Invalid output type'),
    Error(ProcessCode.InvalidPage, "Bad '-pages' argument"),
    Error(ProcessCode.InvalidPage, "Could not parse '-pages' option"),
    Error(ProcessCode.InvalidPage, 'is greater than End page'),
    Error(ProcessCode.InvalidPage, 'is greater than last PDF page'),
    Error(ProcessCode.InvalidPage, 'last PDF page is'),
    Error(ProcessCode.RequestTooLarge, 'Insufficient memory available',
          StatusCode.RequestEntityTooLarge),
    Error(ProcessCode.RequestTooLarge, 'pdf2img ran out of memory',
          StatusCode.RequestEntityTooLarge),
    Error(ProcessCode.InvalidColorModel, 'Invalid color model'),
    Error(ProcessCode.InvalidColorModel,
          'GIF only supports RGB and Gray images'),
    Error(ProcessCode.InvalidCompression, 'Invalid compression type'),
    Error(ProcessCode.InvalidRegion, 'Invalid PDF region type'),
    Error(ProcessCode.InvalidResolution, "'-resolution' bad value specified")]
