"pdfprocess image action errors"

from pdfprocess import Error, ImageProcessCode, ProcessCode, StatusCode


ERRORS = [
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
    Error(ImageProcessCode.InvalidColorModel, 'Invalid color model'),
    Error(ImageProcessCode.InvalidCompression, 'Invalid compression type'),
    Error(ProcessCode.RequestTooLarge, 'Insufficient memory available',
        StatusCode.RequestEntityTooLarge)]

UNKNOWN = Error(ProcessCode.UnknownError, '', StatusCode.InternalServerError)


def _get_errors(stdout):
    result = []
    error_prefix = 'ERROR: '
    for line in str(stdout).split('\n'):
        index = line.find(error_prefix)
        if index < 0: index = line.find(error_prefix.lower())
        if 0 <= index: result.append(line[index + len(error_prefix):])
    return result

def get_error(logger, password, stdout):
    errors = _get_errors(stdout)
    error_string = ''.join([error for error in errors])
    result = next((e for e in ERRORS if e.text in error_string), UNKNOWN)
    if result == UNKNOWN:
        for error in errors: logger(error)
    if result.process_code == ProcessCode.InvalidPassword and password is None:
        result.process_code = ProcessCode.MissingPassword
    return result

