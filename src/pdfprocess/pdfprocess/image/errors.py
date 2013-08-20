"pdfprocess image action errors"

import pdfprocess
from pdfprocess import EnumValue, Error, StatusCode


class ProcessCode(pdfprocess.ProcessCode):
    InvalidColorModel = EnumValue('InvalidColorModel', 21)
    InvalidCompression = EnumValue('InvalidCompression', 22)
    InvalidRegion = EnumValue('InvalidRegion', 23)


ERRORS = [
    Error(ProcessCode.InvalidSyntax, 'An option is missing the = sign'),
    Error(ProcessCode.InvalidSyntax,
        'An option requiring a value has no value supplied.'),
    Error(ProcessCode.InvalidOutputType, 'Invalid output type'),
    Error(ProcessCode.InvalidPage, "Could not parse '-pages' option."),
    Error(ProcessCode.InvalidPage, 'greater than last PDF page'),
    Error(ProcessCode.RequestTooLarge, 'Insufficient memory available',
        StatusCode.RequestEntityTooLarge),
    Error(ProcessCode.InvalidColorModel, 'Invalid color model'),
    Error(ProcessCode.InvalidCompression, 'Invalid compression type'),
    Error(ProcessCode.InvalidRegion, 'Invalid PDF region type')]

