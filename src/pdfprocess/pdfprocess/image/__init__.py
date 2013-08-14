"pdfprocess image package"

import base64
import json
import subprocess
import tempfile

import flask

import errors
import pdfprocess
from pdfprocess import Auth, Error, ProcessCode
from .argument_parser import ArgumentParser, Flag
from .output_file import OutputFile


class Action(pdfprocess.Action):
    def __init__(self, logger, request):
        pdfprocess.Action.__init__(self, logger, request)
        self._input_name = self.request_form.get('inputName', '<anon>')
        self._output_form = self._get_output_form()
        options = self.request_form.get('options', '')
        self._options = json.loads(options) if options else {}
        self._parser = ArgumentParser(self._log_request)
    def __call__(self):
        try:
            self._parser(self._options, self.output_form)
        except Exception as exc:
            return self.abort(Error(ProcessCode.InvalidSyntax, exc.message))
        if self.multipage_request and self.output_form != 'tif':
            exc_info = 'Use TIFF format for multi-page image requests'
            return self.abort(Error(ProcessCode.InvalidPage, exc_info))
        auth = self.authorize()
        if auth in (Auth.OK, Auth.Unknown): return self._pdf2img()
        return self.authorize_error(auth)
    def _get_image(self, input_name, output_file):
        with pdfprocess.Stdout() as stdout:
            options = self._parser.options + output_file.options
            args = ['pdf2img'] + options + [input_name, self.output_form]
            if subprocess.call(args, stdout=stdout):
                logger = self._logger.debug
                password = self.request_form.get('password', None)
                return self.abort(errors.get_error(logger, password, stdout))
        with open(output_file.name, 'rb') as image_file:
            image = base64.b64encode(image_file.read())
            return self.response(ProcessCode.OK, image)
    def _get_output_form(self):
        result = self.request_form.get('outputForm', 'tif').lower()
        if result == 'jpeg': result = 'jpg'
        if result == 'tiff': result = 'tif'
        return result
    def _log_request(self, parser_options):
        input_name = self.input_name
        if ' ' in input_name: input_name = '"%s"' % input_name
        options = ' '.join(parser_options)
        if options: options = ' ' + options
        self._logger.info('pdf2img%s %s %s (%s)' %
            (options, input_name, self.output_form, self.api_key))
    def _pdf2img(self):
        with tempfile.NamedTemporaryFile() as input_file:
            self.input.save(input_file)
            input_file.flush()
            input_name = input_file.name
            pages, output_form = (self.pages, self.output_form)
            with OutputFile(input_name, pages, output_form) as output_file:
                return self._get_image(input_name, output_file)
    @property
    def input_name(self): return self._input_name
    @property
    def multipage_request(self): return '-' in self.pages or ',' in self.pages
    @property
    def output_form(self): return self._output_form
    @property
    def pages(self): return self._parser.pages

