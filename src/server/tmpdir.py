import os
import platform
import tempfile

from errors import UNKNOWN


def _find_dir(dir_name, path=None):
    "return directory on path to root, e.g. /opt/pdfprocess/web-api/tmp"
    path = path or os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(path)
    if parent_dir == path:
        raise UNKNOWN.copy('no {} directory'.format(dir_name))
    path = os.path.join(parent_dir, dir_name)
    return path if os.path.isdir(path) else _find_dir(dir_name, parent_dir)

RESOURCE = _find_dir('Resource') if platform.system() == 'Linux' else None
ROOT_DIR = _find_dir('web-api')
TMP_DIR = _find_dir('tmp')
VAR_DIR = _find_dir('var')

os.environ['TMPDIR'] = TMP_DIR  # for APDFL


class TemporaryFile(object):
    "Facilitates temporary file usage."
    def __init__(self):
        self._file = tempfile.NamedTemporaryFile(dir=TMP_DIR)
    def __del__(self):
        self._file.close()
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        del self
    def __getattr__(self, name):
        return getattr(self._file, name)
    def write(self, str):
        self._file.write(str)
        self._file.flush()

class Stdout(TemporaryFile):
    "For capturing stdout."
    def __str__(self):
        self._file.seek(0)
        return ''.join((line for line in self._file))
    def errors(self):
        "Return the last error message, because it's the most informative."
        result = ''
        error_prefix = 'ERROR: '
        for line in str(self).split('\n'):
            index = line.find(error_prefix)
            if index < 0: index = line.find(error_prefix.lower())
            if 0 <= index: result = line[index + len(error_prefix):]
        return result
