import argparse
import translator
from options import Option, Flag, OPTIONS
from translator import Compression, ImageSize, OutputFormat
from translator import Pages, Resolution, Smoothing


class ArgumentParser(argparse.ArgumentParser):
    "Use argparse.ArgumentParser to parse RenderPages options."
    def __init__(self):
        argparse.ArgumentParser.__init__(self)
        self._compression = Compression()
        self._image_size = ImageSize()
        self._output_format = OutputFormat()
        self._pages = Pages()
        self._resolution = Resolution()
        self._smoothing = Smoothing()
        for option in OPTIONS + translator.OPTIONS:
            self.add_argument(u'-{}'.format(option.name), action=option.action)
    def __call__(self, options):
        self._output_format(options)
        self._set_options(options)
        self.parse_args(self.options)
        self.pdf2img_options.extend(self._compression(options))
        self.pdf2img_options.extend(self._image_size(options))
        self.pdf2img_options.extend(self._pages(options, self.output_format))
        self.pdf2img_options.extend(self._resolution(options))
        self.pdf2img_options.extend(self._smoothing(options))
    def error(self, message):
        "Overrides :py:meth:`argparse.ArgumentParser.error`."
        raise Exception(message)
    def _option_value(self, option_prefix):
        for option in self.options:
            if option.startswith(option_prefix):
                return option[len(option_prefix):]
    def _set_options(self, options):
        self._options, self._pdf2img_options = [], []
        for key, value in options.iteritems():
            if key in OPTIONS and value:
                option = OPTIONS[OPTIONS.index(key)]
                self.options.append(option.format(value))
                self.pdf2img_options.append(option.format(value, True))
            elif key in translator.OPTIONS:
                option = translator.OPTIONS[translator.OPTIONS.index(key)]
                self.options.append(option.format(value))
            elif value is True:
                self.options.append(Flag.FORMAT.format(key))
            elif value:
                self.options.append(Option.FORMAT.format(key, value))
    @property
    def options(self):
        "The WebAPI options list for this request."
        return self._options
    @property
    def output_format(self):
        "The output format for this request, e.g. PNG."
        return self._output_format.option_value
    @property
    def pdf2img_options(self):
        "PDF2IMG options list for this request."
        return self._pdf2img_options
