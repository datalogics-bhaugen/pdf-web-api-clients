"pdfprocess image action arguments"

import argparse


class Option(object):
    def __init__(self, name, help, is_alias=True):
        self._name = name
        self._help = help
        self._is_alias = is_alias
        self._normalized_name = name.lower()
    def __str__(self):
        return self._normalized_name if self._is_alias else self.name
    def __eq__(self, other): return self._normalized_name == other.lower()
    def __ne__(self, other): return not self == other
    @property
    def name(self): return self._name
    @property
    def help(self): return self._help
    @property
    def action(self): return 'store'


class Flag(Option):
    @property
    def action(self): return 'store_true'


OPTIONS = [
    Flag('OPP', 'Enables Overprint Preview in output', is_alias=False),
    Flag('asPrinted', 'Renders annotations as if printing instead of viewing'),
    Flag('blackIsOne', 'Reverse interpretation of B/W pixels (TIFF only)'),
    Flag('noAnnot', 'Suppresses displayable annotations.'),
    Flag('noCMM', 'Suppresses color managed workflow'),
    Flag('noEnhanceThinLines', 'Suppresses "enhance thin lines" option'),
    Option('colorModel', '[gray|cmyk|rgb|rgba] (default=rgb)'),
    Option('compression', '[no|lzw|g3|g4|jpg] (TIFF only, default=lzw)'),
    Option('pages', 'comma-separated or range'),
    Option('password', '127 characters or less, no spaces'),
    Option('pdfRegion', '[crop|media|art|trim|bleed|bounding]'),
    Option('resolution', '[horiz x vert] target DPI, [12-2400] (default=300)'),
    Option('smoothing', '[none|text|all] (default=none)')]


class PixelCount(object):
    OPTIONS = [
        Option('width', 'Picture width (pixels), no default'),
        Option('height', 'Picture height (pixels), no default')]
    def __init__(self):
        self._dimensions = {}
    def __setitem__(self, key, value):
        self._dimensions[key.lower()] = value
    def option(self):
        if len(self._dimensions) == 2:
            return '-pixelcount=%sx%s' % (self.width, self.height)
        elif 'width' in self._dimensions:
            return '-pixelcount=w:%s' % self.width
        elif self._dimensions:
            return '-pixelcount=h:%s' % self.height
    @property
    def width(self): return self._dimensions['width']
    @property
    def height(self): return self._dimensions['height']


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, logger):
        argparse.ArgumentParser.__init__(self, 'actions/image')
        self._logger = logger
        for option in OPTIONS + PixelCount.OPTIONS:
            self.add_argument('-%s' % option.name,
                help=option.help, action=option.action)
    def __call__(self, input_name, output_form, options):
        self._set_options(options)
        self._log_request(input_name, output_form)
        self.parse_args(self.options)
        self._set_pages(output_form)
    def error(self, message):
        "overrides argparse.ArgumentParser.error"
        raise Exception(message)
    def _log_request(self, input_name, output_form):
        options = ' '.join(self.options)
        if options: options = ' ' + options
        if ' ' in input_name: input_name = '"%s"' % input_name
        self._logger.info('pdf2img%s %s %s' %
            (options, input_name, output_form))
    def _pixel_count_option(self, options):
        pixel_count = PixelCount()
        for key, value in options.iteritems():
            if key in PixelCount.OPTIONS: pixel_count[key] = value
        return pixel_count.option()
    def _set_options(self, options):
        flag_syntax, name_value_syntax = ('-%s', '-%s=%s')
        pixel_count_option = self._pixel_count_option(options)
        self._options = [pixel_count_option] if pixel_count_option else []
        # TODO: transform options as specified in Matt's Basecamp comment
        for key, value in options.iteritems():
            if key in PixelCount.OPTIONS: continue
            option = OPTIONS[OPTIONS.index(key)] if key in OPTIONS else None
            if isinstance(option, Flag):
                self.options.append(flag_syntax % option)
            elif isinstance(option, Option):
                self.options.append(name_value_syntax % (option, value))
            elif value is True:
                self.options.append(flag_syntax % key)
            else:
                self.options.append(name_value_syntax % (key, value))
    def _set_pages(self, output_form):
        pages_prefix = '-pages='
        for option in self.options:
            if option.startswith(pages_prefix):
                self._pages = option[len(pages_prefix):]
                return
        if output_form != 'tif':
            self._pages = '1'
            self._options.append(pages_prefix + self.pages)
    @property
    def options(self): return self._options
    @property
    def pages(self): return self._pages

