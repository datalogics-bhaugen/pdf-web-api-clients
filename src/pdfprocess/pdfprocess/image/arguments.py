'API image arguments'

import argparse

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
    def __init__(self, args=None):
        'args defaults to sys.argv'
        self._args = args
        self._parser = argparse.ArgumentParser(__file__)
        self._parser.add_argument('inputFile', help='PDF or XPS file')
        self._parser.add_argument('outputForm',
            help='EPS, TIF, JPG, BMP, PNG, GIF, RAW, or PDF')
        for option in OPTIONS:
            option_name = '-' + option.name
            self._parser.add_argument(option_name,
                help=option.help, action=option.action)
    def __call__(self):
        self._namespace = self._parser.parse_args(self._args)
    def __getitem__(self, key):
        return self._namespace.__dict__[key]
    @classmethod
    def options(cls): return OPTIONS

