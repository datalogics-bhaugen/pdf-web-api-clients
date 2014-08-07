#!/usr/bin/env python

'''
usage: stress.py request_type input_index [minutes]
e.g.: stress.py FlattenForm FlattenForm.cfg 66
'''

import os
import sys
import time
import json
import random
import inspect
import ConfigParser

import cfg
import test_client


class Input(object):
    def __init__(self, directory, filename, pages):
        "filenames in index must be relative to index's filename"
        self._filename = os.path.join(directory, filename)
        self._pages = int(pages)
    @classmethod
    def list(cls, index):
        result = []
        directory = os.path.dirname(index)
        parser = ConfigParser.ConfigParser()
        parser.optionxform = str
        parser.read(index)
        for section in parser.sections():
            for filename, pages in parser.items(section):
                result.append(Input(directory, filename, pages))
        return result
    @property
    def filename(self): return self._filename
    @property
    def pages(self): return self._pages


class Test(object):
    def __init__(self, input):
        self._input = input
    def _args(self):
        return [self._input.filename]
    @classmethod
    def type(cls, request_type):
        is_test_type =\
            lambda m: inspect.isclass(m) and m.__name__ == request_type
        members = inspect.getmembers(sys.modules[__name__], is_test_type)
        return members[0][1] if members else type(request_type, (Test,), {})
    @property
    def args(self): return [__file__, self.__class__.__name__] + self._args()
    @property
    def port(self): return 8080

class FillForm(Test):
    def _args(self):
        forms_data = self._input.filename
        return [os.path.splitext(forms_data)[0] + '.pdf', forms_data]

class RenderPages(Test):
    def _args(self):
        pages = self._input.pages
        pages = 1 if pages < 2 else random.randrange(1, pages)
        options = {'pages': pages, 'pdfRegion': 'media', 'resolution': 200}
        return Test._args(self) + ['options={}'.format(json.dumps(options))]
    @property
    def port(self): return cfg.Configuration.service.port

# TODO: support new request types by defining new Test classes as needed


def stress(test_class, input_list, minutes):
    result = 0
    end = time.time() + minutes * 60
    while (time.time() < end):
        try:
            test = test_class(input_list[random.randrange(0, len(input_list))])
            test_client.run(test.args, 'http://127.0.0.1:{}'.format(test.port))
            result += 1
        except:
            pass
    return result

if __name__ == '__main__':
    if len(sys.argv) < 3: raise Exception(__doc__)
    test_class = Test.type(sys.argv[1])
    input_list = Input.list(sys.argv[2])
    minutes = float(sys.argv[3] if len(sys.argv) > 3 else 66)
    print('#tests: {}'.format(stress(test_class, input_list, minutes)))
