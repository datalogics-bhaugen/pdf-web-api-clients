"web_api pdf2img action arguments"

import argparse
import translator
from options import Option, Flag, OPTIONS
from translator import ImageSize, OutputFormat, Pages, Resolution, Smoothing


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, request_logger):
        argparse.ArgumentParser.__init__(self, 'actions/render/pages')
        self._request_logger = request_logger
        self._image_size = ImageSize()
        self._output_format = OutputFormat()
        self._pages = Pages()
        self._resolution = Resolution()
        self._smoothing = Smoothing()
        for option in OPTIONS + translator.OPTIONS:
            self.add_argument('-%s' % option.name, action=option.action)
    def __call__(self, options):
        self._output_format(options)
        self._set_options(options)
        self._request_logger(self.options)
        self.parse_args(self.options)
        self.pdf2img_options.extend(self._image_size(options))
        self.pdf2img_options.extend(self._pages(options, self.output_format))
        self.pdf2img_options.extend(self._resolution(options))
        self.pdf2img_options.extend(self._smoothing(options))
    def error(self, message):
        "overrides argparse.ArgumentParser.error"
        raise Exception(message)
    def _option_value(self, option_prefix):
        for option in self.options:
            if option.startswith(option_prefix):
                return option[len(option_prefix):]
    def _set_options(self, options):
        self._options, self._pdf2img_options = [], []
        for key, value in options.iteritems():
            if key in OPTIONS:
                option = OPTIONS[OPTIONS.index(key)]
                self.pdf2img_options.append(option.format(value, True))
                self.options.append(option.format(value))
            elif key in translator.OPTIONS:
                option = translator.OPTIONS[translator.OPTIONS.index(key)]
                self.options.append(option.format(value))
            elif value is True:
                self.options.append(Flag.FORMAT % key)
            else:
                self.options.append(Option.FORMAT % (key, value))
    @property
    def options(self): return self._options
    @property
    def output_format(self): return self._output_format.option
    @property
    def pages(self): return self._pages.option
    @property
    def pdf2img_options(self): return self._pdf2img_options
