#!/usr/bin/env python

'''
usage: stress.py request_type document_index [minutes]
e.g.: stress.py FlattenForm test_set.cfg 66
'''

import os
import sys
import time
import random
import ConfigParser
import simplejson as json

import test_client


RENDER_PAGES_OPTIONS = {'pdfRegion': 'media', 'resolution': 200}

class Document(object):
    def __init__(self, directory, filename, pages):
        self._filename = os.path.join(directory, filename)
        self._pages = int(pages)
    @property
    def filename(self): return self._filename
    @property
    def pages(self): return self._pages

def documents(document_index):
    result = []
    directory = os.path.dirname(document_index)
    parser = ConfigParser.ConfigParser()
    parser.optionxform = str
    parser.read(document_index)
    for section in parser.sections():
        for filename, pages in parser.items(section):
            result.append(Document(directory, filename, pages))
    return result

def stress(request_type, minutes, documents):
    result = 0
    end = time.time() + minutes * 60
    while (time.time() < end):
        try:
            random_document = documents[random.randrange(0, len(documents))]
            args, base_url = test_client_args(request_type, random_document)
            test_client.run(args, base_url)
            result += 1
        except:
            pass
    return result

def test_client_args(request_type, document):
    args, port = [__file__, request_type, document.filename], 8080
    if request_type == 'RenderPages':
        options, pages = RENDER_PAGES_OPTIONS, document.pages
        random_page = 1 if pages < 2 else random.randrange(1, pages)
        options.update({'pages': str(random_page)})
        args.append('options={}'.format(json.dumps(options)))
        port = 5000
    return args, 'http://127.0.0.1:{}'.format(port)

if __name__ == '__main__':
    if len(sys.argv) < 3: raise Exception(__doc__)
    request_type, document_index = sys.argv[1], sys.argv[2]
    minutes = float(sys.argv[3] if len(sys.argv) > 3 else 66)
    stress_tests = stress(request_type, minutes, documents(document_index))
    print('#tests: {}'.format(stress_tests))
