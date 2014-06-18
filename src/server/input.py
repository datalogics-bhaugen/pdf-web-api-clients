"WebAPI input document"

import abc
import requests

from cfg import Configuration
from errors import Error, ErrorCode, HTTPCode


class ChunkedTransfer(object):
    "uses chunked transfer logic to enforce input size limit"
    def __init__(self, from_url, to_file):
        self._input, self._to_file = None, None
        try:
            self._input = requests.get(from_url, stream=True)
        except Exception as exception:
            raise Error(ErrorCode.InvalidInput, unicode(exception))
        self._validate_input_size(self._content_length())
        self._transfer(to_file)
        self._to_file = to_file
    def __del__(self):
        if self._input: self._input.close()
    def _content_length(self):
        try:
            return int(self._input.headers['content-length'])
        except:
            return 0
    def _transfer(self, to_file):
        for chunk in self._input.iter_content(chunk_size=self.chunk_size):
            if chunk:
                to_file.write(chunk)
                self._validate_input_size(to_file.tell())
    def _validate_input_size(self, input_size):
        if input_size > self.max_input_size:
            raise Error(ErrorCode.InvalidInput,
                        'input too large (max={})'.format(self.max_input_size),
                        HTTPCode.RequestEntityTooLarge)
    @property
    def chunk_size(self): return self.max_input_size / 10
    @property
    def file(self): return self._to_file
    @property
    def max_input_size(self): return int(Configuration.limits.input_size)


class Input(object):
    "each request input class should inherit from this class"
    __metaclass__ = abc.ABCMeta
    def __init__(self, action):
        self._action, self._input = action, None
    @abc.abstractmethod
    def initialize(self):
        pass
    @abc.abstractmethod
    def save(self):
        pass
    def _raise_error(self, error):
        self._action.raise_error(Error(ErrorCode.InvalidInput, error))
    @property
    def files(self): return self._action.request_files

class FromInput(Input):
    "for input extracted from an input form part"
    def initialize(self):
        files = len(self.files)
        if files > 1:
            self._raise_error(u'excess input ({} files)'.format(files))
        if 'input' not in self.files:
            self._raise_error(u'request missing "input" or "inputURL" part')
        self._input = self.files['input']
    def save(self, input_file):
        self._input.save(input_file)

class FromInputURL(Input):
    "for input specified by an inputURL form part"
    def initialize(self):
        if self.files:
            self._raise_error(u'excess input (inputURL and request file)')
    def save(self, input_file):
        ChunkedTransfer(self._action.input_url, input_file)
