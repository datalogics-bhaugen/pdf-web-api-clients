"pdfprocess image action arguments"

import argparse
from options import Flag, ImageSize, Option, OPTIONS


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, logger):
        argparse.ArgumentParser.__init__(self, 'actions/image')
        self._logger = logger
        for option in OPTIONS + ImageSize.OPTIONS:
            self.add_argument('-%s' % option.name, action=option.action)
    def __call__(self, options):
        self._set_options(options)
        self._set_output_form(options)
        self._logger(self.options)
        self.parse_args(self.options)
        self._pages = self._get_pages()
        self._add_smoothing_option()
    def error(self, message):
        "overrides argparse.ArgumentParser.error"
        raise Exception(message)
    def _add_smoothing_option(self):
        smoothing_prefix = '-smoothing='
        smoothing = self._option_value(smoothing_prefix)
        if not smoothing: self.options.append(smoothing_prefix + 'all')
    def _get_output_form(self, options):
        for key, value in options.iteritems():
            if key.lower() == 'outputform':
                return value.lower()
    def _get_pages(self):
        pages_prefix = '-pages='
        result = self._option_value(pages_prefix)
        if result: return result
        result = '' if self.output_form == 'tif' else '1'
        if result: self._options.append(pages_prefix + result)
        return result
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
        flag_syntax, option_syntax = ('-%s', '-%s=%s')
        self._options = self._image_size_options(options)
        self._pdf2img_options = list(self.options)
        for key, value in options.iteritems():
            if key in ImageSize.OPTIONS or key == 'outputForm': continue
            option = OPTIONS[OPTIONS.index(key)] if key in OPTIONS else None
            if isinstance(option, Flag):
                if value:
                    self.options.append(flag_syntax % option.name)
                    self.pdf2img_options.append(flag_syntax % option)
            elif isinstance(option, Option):
                self.options.append(option_syntax % (option.name, value))
                self.pdf2img_options.append(option_syntax % (option, value))
            elif value is True:
                self.options.append(flag_syntax % key)
                self.pdf2img_options.append(flag_syntax % key)
            else:
                self.options.append(option_syntax % (key, value))
                self.pdf2img_options.append(option_syntax % (key, value))
    def _set_output_form(self, options):
        output_form = self._get_output_form(options)
        if output_form == 'jpeg': output_form = 'jpg'
        if output_form == 'tiff': output_form = 'tif'
        self._output_form = output_form or 'tif'
    @property
    def options(self): return self._options
    @property
    def output_form(self): return self._output_form
    @property
    def pages(self): return self._pages
    @property
    def pdf2img_options(self): return self._pdf2img_options

