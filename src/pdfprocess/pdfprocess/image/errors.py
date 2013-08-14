"pdfprocess image errors"

from pdfprocess import Error, ProcessCode, StatusCode


ERRORS = [
    Error(ProcessCode.InvalidInput, "File does not begin with '%PDF-'.",
        StatusCode.UnsupportedMediaType),
    Error(ProcessCode.InvalidInput,
        'The file is damaged and could not be repaired.'),
    Error(ProcessCode.MissingPassword, 'missing_password',
        StatusCode.Forbidden),
    Error(ProcessCode.InvalidPassword, 'invalid_password',
        StatusCode.Forbidden),
    Error(ProcessCode.AdeptDRM,
        'The security plug-in required by this command is unavailable.',
        StatusCode.Forbidden),
    Error(ProcessCode.InvalidOutputType, 'Invalid output type'),
    Error(ProcessCode.InvalidPage, "Could not parse '-pages' option."),
    Error(ProcessCode.InvalidPage, 'greater than last PDF page'),
    Error(ProcessCode.RequestTooLarge, 'Insufficient memory available',
        StatusCode.RequestEntityTooLarge)]

UNKNOWN = Error(ProcessCode.UnknownError, '', StatusCode.InternalServerError)


def _get_errors(stdout):
    errors = []
    error_prefix = 'ERROR: '
    for line in str(stdout).split('\n'):
        index = line.find(error_prefix)
        if index < 0: index = line.find(error_prefix.lower())
        if 0 <= index: errors.append(line[index + len(error_prefix):])
    return '\n'.join([error for error in errors])

def get_error(logger, stdout):
    errors = _get_errors(stdout)
    result = next((e for e in ERRORS if e.text in errors), UNKNOWN)
    if result == UNKNOWN: logger(errors)
    return result

