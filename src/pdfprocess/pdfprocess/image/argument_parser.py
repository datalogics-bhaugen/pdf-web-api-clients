"pdfprocess image action arguments"

import argparse
import translator
from options import Option, Flag, OPTIONS
from translator import ImageSize, OutputForm, Resolution, Smoothing


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, request_logger):
        argparse.ArgumentParser.__init__(self, 'actions/image')
        self._request_logger = request_logger
        self._image_size, self._output_form = (ImageSize(), OutputForm())
        self._resolution, self._smoothing = (Resolution(), Smoothing())
        for option in OPTIONS + translator.OPTIONS:
            self.add_argument('-%s' % option.name, action=option.action)
    def __call__(self, options):
        self._set_options(options)
        self._request_logger(self.options)
        self.parse_args(self.options)
        self.pdf2img_options.extend(self._image_size(options))
        self.pdf2img_options.extend(self._resolution(options))
        self.pdf2img_options.extend(self._smoothing(options))
        self._output_form(options)
        self._pages = self._get_pages()
    def error(self, message):
        "overrides argparse.ArgumentParser.error"
        raise Exception(message)
    def _get_pages(self):
        pages_prefix = '-pages='
        result = self._option_value(pages_prefix)
        if result: return result
        result = '' if self.output_form == 'tif' else '1'
        if result: self.pdf2img_options.append(pages_prefix + result)
        return result
    def _option_value(self, option_prefix):
        for option in self.options:
            if option.startswith(option_prefix):
                return option[len(option_prefix):]
    def _set_options(self, options):
        flag_syntax, option_syntax = ('-%s', '-%s=%s')
        self._options, self._pdf2img_options = ([], [])
        pdf2img_options, all_options = (OPTIONS, OPTIONS + translator.OPTIONS)
        for key, value in options.iteritems():
            if key in pdf2img_options:
                option = pdf2img_options[pdf2img_options.index(key)]
                if value is True:
                    pdf2img_option = flag_syntax % option
                elif not isinstance(option, Flag):
                    pdf2img_option = option_syntax % (option, value)
                self.pdf2img_options.append(pdf2img_option)
            if key in all_options:
                option = all_options[all_options.index(key)]
                if value is True:
                    self.options.append(flag_syntax % option.name)
                elif not isinstance(option, Flag):
                    self.options.append(option_syntax % (option.name, value))
            elif value is True:
                self.options.append(flag_syntax % key)
            else:
                self.options.append(option_syntax % (key, value))
    @property
    def options(self): return self._options
    @property
    def output_form(self): return self._output_form.option
    @property
    def pages(self): return self._pages
    @property
    def pdf2img_options(self): return self._pdf2img_options

