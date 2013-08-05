import tempfile


class Stdout(object):
    "for capturing stdout"
    def __init__(self):
        self._file = tempfile.TemporaryFile()
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self._file.close()
    def __str__(self):
        self._file.seek(0)
        return ''.join((line for line in self._file))
    def __getattr__(self, name):
        return getattr(self._file, name)

