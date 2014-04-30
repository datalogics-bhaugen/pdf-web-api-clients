"WebAPI input document"

import requests

from StringIO import StringIO
from cfg import Configuration
from errors import Error, ErrorCode


class ChunkedTransfer(object):
    def __init__(self, from_url, to_file):
        self._file, self._input = None, None
        try:
            self._input = requests.get(from_url, stream=True)
        except Exception as exception:
            raise Error(ErrorCode.InvalidInput, unicode(exception))
        self._transfer(to_file)
    def __del__(self):
        if self._input: self._input.close()
    def _content_length(self):
        try:
            return int(self._input.headers['content-length'])
        except:
            return 0
    def _transfer(self, to_file):
        Error.validate_input_size(self._content_length())
        chunk_size = int(Configuration.limits.input_size) / 10
        for chunk in self._input.iter_content(chunk_size=chunk_size):
            if chunk:
                to_file.write(chunk)
                Error.validate_input_size(to_file.tell())
        self._file = to_file
    @property
    def file(self):
        return self._file


class Input(object):
    def __init__(self, action):
        self._action, self._input = action, None
    def _raise_error(self, error):
        self._action.raise_error(Error(ErrorCode.InvalidInput, error))
    @property
    def files(self): return self._action.request_files

class FromForm(Input):
    def initialize(self):
        files = len(self.files)
        if files > 1:
            self._raise_error(u'excess input ({} files)'.format(files))
        if 'input' not in self.files:
            self._raise_error(u'request missing "input" or "inputURL" part')
        self._input = self.files['input']
    def save(self, input_file):
        self._input.save(input_file)

class FromURL(Input):
    def initialize(self):
        if self.files:
            self._raise_error(u'excess input (inputURL and request file)')
    def save(self, input_file):
        ChunkedTransfer(self._action.input_url, input_file)


class InputFile(StringIO):
    def __init__(self, input_url):
        StringIO.__init__(self)
        self._input_url = input_url
        ChunkedTransfer(input_url, self)
    @property
    def name(self):
        return self._input_url
