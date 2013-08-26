"pdfprocess image action errors"

import pdfprocess
from pdfprocess import EnumValue, Error, StatusCode


class ProcessCode(pdfprocess.ProcessCode):
    InvalidColorModel = EnumValue('InvalidColorModel', 21)
    InvalidCompression = EnumValue('InvalidCompression', 22)
    InvalidRegion = EnumValue('InvalidRegion', 23)
    InvalidResolution = EnumValue('InvalidResolution', 24)


ERRORS = [
    Error(ProcessCode.InvalidSyntax, 'An option is missing the = sign'),
    Error(ProcessCode.InvalidSyntax,
        'An option requiring a value has no value supplied'),
    Error(ProcessCode.InvalidOutputType, 'Invalid output type'),
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

