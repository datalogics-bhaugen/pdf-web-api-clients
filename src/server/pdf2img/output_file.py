import os
import glob
from server import UNKNOWN


class OutputFile(object):
    '''
    PDF2IMG appends a page number to the output filename, so we cannot
    use the *tempfile* module to construct the output file. Instead,
    we assume that PDF2IMG successfully created the output file from
    the temporary file we provided as input. This class encapsulates
    all this logic, and deletes the image files created by PDF2IMG.
    '''
    def __init__(self, input_filename, output_extension):
        self._pattern = '{}*.{}'.format(input_filename, output_extension)
    def __del__(self):
        for filename in self._glob():
            try: os.remove(filename)
            except Exception: pass
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        pass
    def _glob(self):
        return glob.glob(self._pattern)
    @property
    def name(self):
        "The PDF2IMG output filename."
        names = self._glob()
        if len(names) == 1: return names[0]
        message = 'unsupported multi-page image request' if names else None
        raise UNKNOWN.copy(message)
