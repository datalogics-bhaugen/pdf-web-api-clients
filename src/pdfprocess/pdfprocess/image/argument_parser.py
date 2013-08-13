"pdfprocess image action arguments"

import argparse


class Option(object):
    def __init__(self, name, normalize=True):
        self._name = name
        self._normalize = normalize
        self._normalized_name = name.lower()
    def __str__(self):
        return self._normalized_name if self._normalize else self.name
    def __eq__(self, other): return self._normalized_name == other.lower()
    def __ne__(self, other): return not self == other
    @property
    def name(self): return self._name
    @property
    def action(self): return 'store'


class Flag(Option):
    @property
    def action(self): return 'store_true'

class FlagAlias(Flag):
    def __init__(self, name, pdf2img_name):
        Flag.__init__(self, name)
        self._pdf2img_name = pdf2img_name.lower()
    def __str__(self):
        return self._pdf2img_name


OPTIONS = [
    Flag('OPP', normalize=False),
    FlagAlias('disableColorManagement', 'noCMM'),
    FlagAlias('disableThinLineEnhancement', 'noEnhanceThinLines'),
    FlagAlias('printPreview', 'asPrinted'),
    FlagAlias('suppressAnnotations', 'noAnnot'),
    Option('colorModel'),
    Option('compression'),
    Option('pages'),
    Option('password'),
    Option('pdfRegion'),
    Option('resolution'),
    Option('smoothing')]


class ImageSize(object):
    OPTIONS = [Option('width'), Option('height')]
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
        for option in OPTIONS + ImageSize.OPTIONS:
            self.add_argument('-%s' % option.name, action=option.action)
    def __call__(self, options, output_form):
        self._set_options(options)
        self._logger(self.options)
        self.parse_args(self.options)
        self._pages = self._get_pages(output_form)
        self._add_smoothing_option()
    def error(self, message):
        "overrides argparse.ArgumentParser.error"
        raise Exception(message)
    def _add_smoothing_option(self):
        smoothing_prefix = '-smoothing='
        smoothing = self._option_value(smoothing_prefix)
        if not smoothing: self.options.append(smoothing_prefix + 'all')
    def _get_pages(self, output_form):
        pages_prefix = '-pages='
        pages = self._option_value(pages_prefix)
        if pages: return pages
        pages = '' if output_form == 'tif' else '1'
        if pages: self._options.append(pages_prefix + pages)
        return pages
    def _image_size_options(self, options):
        image_size = ImageSize()
        for key, value in options.iteritems():
            if key in ImageSize.OPTIONS: image_size[key] = value
        return image_size.options()
    def _option_value(self, option_prefix):
        for option in self.options:
            if option.startswith(option_prefix):
                return option[len(option_prefix):]
    def _set_options(self, options):
        flag_syntax, name_value_syntax = ('-%s', '-%s=%s')
        self._options = self._image_size_options(options)
        for key, value in options.iteritems():
            if key in ImageSize.OPTIONS: continue
            option = OPTIONS[OPTIONS.index(key)] if key in OPTIONS else None
            if isinstance(option, Flag):
                if value: self.options.append(flag_syntax % option)
            elif isinstance(option, Option):
                self.options.append(name_value_syntax % (option, value))
            elif value is True:
                self.options.append(flag_syntax % key)
            else:
                self.options.append(name_value_syntax % (key, value))
    @property
    def options(self): return self._options
    @property
    def pages(self): return self._pages

