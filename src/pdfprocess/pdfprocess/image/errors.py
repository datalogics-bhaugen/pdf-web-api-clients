"pdfprocess image action errors"

import pdfprocess
from pdfprocess import EnumValue, Error, StatusCode


class ProcessCode(pdfprocess.ProcessCode):
    InvalidColorModel = EnumValue('InvalidColorModel', 21)
    InvalidCompression = EnumValue('InvalidCompression', 22)
    InvalidRegion = EnumValue('InvalidRegion', 23)


ERRORS = pdfprocess.ERRORS + [
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

UNKNOWN = Error(ProcessCode.UnknownError, '', StatusCode.InternalServerError)


def get_error(logger, stdout):
    errors = _get_errors(stdout)
    error_text = ' '.join([error for error in errors])
    try:
        error = next(e for e in ERRORS if e.text in error_text)
        return error.copy(error_text)
    except StopIteration:
        for error in errors: logger(error)
        return UNKNOWN

def _get_errors(stdout):
    result = []
    error_prefix = 'ERROR: '
    for line in str(stdout).split('\n'):
        index = line.find(error_prefix)
        if index < 0: index = line.find(error_prefix.lower())
        if 0 <= index: result.append(line[index + len(error_prefix):])
    return result

