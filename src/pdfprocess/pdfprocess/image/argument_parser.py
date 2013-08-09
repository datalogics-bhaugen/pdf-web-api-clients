"pdfprocess image action arguments"

import argparse


class Option(object):
    def __init__(self, name, help, is_alias=True):
        self._name = name
        self._help = help
        self._is_alias = is_alias
        self._normalized_name = name.lower()
    def __str__(self):
        return '-' + self._normalized_name if self._is_alias else self.name
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
    def options(self):
        if len(self._dimensions) == 2:
            return ['-pixelcount=%sx%s' % (self.width, self.height)]
        elif 'width' in self._dimensions:
            return ['-pixelcount=w:%s' % self.width]
        elif self._dimensions:
            return ['-pixelcount=h:%s' % self.height]
        else:
            return []
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
    def __call__(self, input_file, output_form, request_form):
        self._set_options(request_form)
        self._log_request(input_file, output_form)
        self.parse_args(self.options)
    def error(self, message):
        "overrides argparse.ArgumentParser.error"
        raise Exception(message)
    def _log_request(self, input_file, output_form):
        options = ' '.join(self.options)
        if options: options = ' ' + options
        if ' ' in input_file: input_file = '"%s"' % input_file
        self._logger.info('pdf2img%s %s %s' %
            (options, input_file, output_form))
    def _set_options(self, request_form):
        self._set_pixelcount_option(request_form)
        # TODO: transform options as specified in Matt's Basecamp comment
        for key, value in request_form.iteritems():
            if key in ('apiKey', 'inputFile', 'outputForm'): continue
            if key in OPTIONS:
                option = OPTIONS[OPTIONS.index(key)]
            else:
                option = '-%s' % key
            if not isinstance(option, Flag):
                # option is an Option or it's not recognized
                self._options.append('%s=%s' % (option, value))
            elif value and value != '0' and value.lower() != 'false':
                # option is a Flag and we interpret the value as True
                self._options.append(str(option))
    def _set_pixelcount_option(self, request_form):
        pixel_count = PixelCount()
        for key, value in request_form.iteritems():
            if key in PixelCount.OPTIONS:
                pixel_count[key] = value
        self._options = pixel_count.options()
    @property
    def options(self): return self._options

