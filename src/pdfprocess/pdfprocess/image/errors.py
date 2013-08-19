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
    Error(ProcessCode.InvalidInput, "File does not begin with '%PDF-'.",
        StatusCode.UnsupportedMediaType),
    Error(ProcessCode.InvalidInput,
        'The file is damaged and could not be repaired.'),
    Error(ProcessCode.InvalidPassword, 'This document requires authentication',
        StatusCode.Forbidden),
    Error(ProcessCode.AdeptDRM,
        'The security plug-in required by this command is unavailable.',
        StatusCode.Forbidden),
    Error(ProcessCode.InvalidOutputType, 'Invalid output type'),
    Error(ProcessCode.InvalidPage, "Could not parse '-pages' option."),
    Error(ProcessCode.InvalidPage, 'greater than last PDF page'),
    Error(ProcessCode.RequestTooLarge, 'Insufficient memory available',
        StatusCode.RequestEntityTooLarge),
    Error(ProcessCode.InvalidColorModel, 'Invalid color model'),
    Error(ProcessCode.InvalidCompression, 'Invalid compression type'),
    Error(ProcessCode.InvalidRegion, 'Invalid PDF region type')]

UNKNOWN = Error(ProcessCode.UnknownError, '', StatusCode.InternalServerError)


def get_error(logger, no_password, stdout):
    errors = _get_errors(stdout)
    error_string = ''.join([error for error in errors])
    result = next((e for e in ERRORS if e.text in error_string), UNKNOWN)
    if result == UNKNOWN:
        for error in errors: logger(error)
    if result.process_code == ProcessCode.InvalidPassword and no_password:
        result.process_code = ProcessCode.MissingPassword
    return result

def _get_errors(stdout):
    result = []
    error_prefix = 'ERROR: '
    for line in str(stdout).split('\n'):
        index = line.find(error_prefix)
        if index < 0: index = line.find(error_prefix.lower())
        if 0 <= index: result.append(line[index + len(error_prefix):])
    return result

