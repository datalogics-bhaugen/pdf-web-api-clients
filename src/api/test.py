#!/usr/bin/env python

'web api test client'

import argparse
import exceptions
import os
import requests

FELIX = '10.2.3.86'
JOHN = '10.2.3.11'

ADDRESS = FELIX
PORT = 5000

API_KEY = 'f54ab5d8-5775-42c7-b888-f074ba892b57'

class Option(object):
    def __init__(self, name, help, is_alias=True):
        self._name = name
        self._help = help
        self._is_alias = is_alias
    def __str__(self):
        return '-' + self.name.lower() if self._is_alias else self.name
    @property
    def name(self): return self._name
    @property
    def help(self): return self._help
    @property
    def action(self): return 'store'

class Flag(Option):
    def __init__(self, name, help, is_alias=True):
        Option.__init__(self, name, help)
    @property
    def action(self): return 'store_true'

OPTIONS = [
    Flag('OPP', 'Enables Overprint Preview in output', is_alias=False),
    Flag('asPrinted', 'Renders annotations as if printing instead of viewing'),
    Flag('blackIsOne', 'Reverse interpretation of B/W pixels (TIFF only)'),
    Flag('multiPage', 'Create one multipage file (TIFF only)'),
    Flag('noAnnot', 'Suppresses displayable annotations.'),
    Flag('noCMM', 'Suppresses color managed workflow'),
    Flag('noEnhanceThinLines', 'Suppresses "enhance thin lines" option'),
    Flag('reverse', 'Reverse black for white (grayscale images only)'),
    Option('BPC', '[1 or 8] bits per color channel (default=8)'),
    Option('colorModel', '[gray|cmyk|rgb|rgba] (default=rgb)'),
    Option('compression', '[no|lzw|g3|g4|jpg] (TIFF only, default=lzw)'),
    Option('fontList', '"dir1;dir2;dirN" (see documentation for defaults)'),
    Option('height', 'Picture height (pixels), no default'),
    Option('jpegQuality', '[1 - 100] higher values give larger file sizes'),
    Option('maxBandMem', '[1000000 - 2100000000] (default=300000000)'),
    Option('output', '(default=input filename)'),
    Option('pages', 'comma-separated or range'),
    Option('password', '127 characters or less, no spaces'),
    Option('pdfRegion', '[crop|media|art|trim|bleed|bounding]'),
    Option('resolution', '[horiz x vert] target DPI, [12-2400] (default=300)'),
    Option('smoothing', '[none|text|all] (default=none)'),
    Option('width', 'Picture width (pixels), no default')]

class Arguments():
    def __init__(self):
        parser = argparse.ArgumentParser(__doc__)
        parser.add_argument('inputFile', help='PDF or XPS file')
        parser.add_argument('outputForm',
            help='EPS, TIF, JPG, BMP, PNG, GIF, RAW, or PDF')
        for opt in OPTIONS:
            opt_name = '-' + opt.name
            parser.add_argument(opt_name, help=opt.help, action=opt.action)
        self._namespace = parser.parse_args()
    def __getitem__(self, key):
        return self._namespace.__dict__[key]

def make_request_data(arguments):
    result = {'apiKey': API_KEY,
        'inputFile': arguments['inputFile'],
        'outputForm': arguments['outputForm']}
    for option in OPTIONS:
        if option.name in ('height', 'width', 'output'): continue
        value = arguments[option.name]
        if not value: continue
        result[str(option)] = value
    # TODO: translate height and/or width to pixelcount
    return result

def make_url():
    server = '%s:%d' % (ADDRESS, PORT) if PORT else ADDRESS
    return 'http://%s/0/actions/image' % server

def post_request(arguments):
    data = make_request_data(arguments)
    with open(arguments['inputFile'], 'rb') as input:
        return requests.post(make_url(), data=data, files={'file': input})

def image_name(arguments):
    result = arguments['output']
    if not result:
        result = os.path.splitext(arguments['inputFile'])[0]
        extension = arguments['outputForm'].lower()
        if extension == 'jpeg': extension = 'jpg'
        result += '.' + extension
    return result

def write_image(arguments, image):
    result = image_name(arguments)
    with open(result, 'wb') as output:
        output.write(image)
    return result

def show_image(image):
    try:
        import Image
        Image.open(image).show()
    except ImportError:
        pass

def validate_content_type(arguments, response):
    if arguments['outputForm'] in ('jpeg', 'jpg'):
        assert response.headers['content-type'] == 'image/jpeg'

if __name__ == '__main__':
    arguments = Arguments()
    response = post_request(arguments)
    validate_content_type(arguments, response)
    output = write_image(arguments, response.content)
    show_image(output)

