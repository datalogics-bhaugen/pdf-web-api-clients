import os
import glob
from server import UNKNOWN


class OutputFile(object):
    '''
    PDF2IMG appends a page number to the output filename, so we cannot
    use tempfile to construct the output file. Instead, we assume that
    PDF2IMG successfully created the output file from the temporary
    file we provided as input. This class encapsulates all this logic,
    and deletes the image files created by PDF2IMG.
    '''
    def __init__(self, name, extension):
        self._pattern = '{}*.{}'.format(name, extension)
    def __del__(self):
        for filename in self.glob():
            try: os.remove(filename)
            except Exception: pass
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        pass
    def glob(self):
        return glob.glob(self._pattern)
    @property
    def name(self):
        names = self.glob()
        if len(names) == 1: return names[0]
        message = 'unsupported multi-page image request' if names else None
        raise UNKNOWN.copy(message)
