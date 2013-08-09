"pdfprocess image package"

import base64
import json
import subprocess
import tempfile

import flask

import pdfprocess
from pdfprocess import Auth
from .argument_parser import ArgumentParser, Flag
from .output_file import OutputFile


class Action(pdfprocess.Action):
    def __init__(self, logger, request):
        pdfprocess.Action.__init__(self, logger, request)
        self._input_name = self.request_form.get('inputName', '<anon>')
        self._output_form = self._get_output_form()
        options = self.request_form.get('options', '')
        self._options = json.loads(options) if options else {}
        default_pages = '' if self.tif_request else '1'
        self._pages = self.request_form.get('pages', default_pages)
        self._parser = ArgumentParser(logger)
    def __call__(self):
        try:
            self._parser(self.input_name, self.output_form, self._options)
        except Exception as exc:
            return self.abort(-1, exc.message) # TODO: process_code
        if self.multipage_request and not self.tif_request:
            TODO = 666
            exc_info = 'Use TIFF format for multi-page image requests'
            return self.abort(TODO, exc_info)
        auth = self.authorize()
        if auth in (Auth.Ok, Auth.Unknown): return self._pdf2img()
        return self.authorize_error(auth)
    def _get_image(self, input_name, output_file):
        options = self._parser.options + output_file.options
        args = ['pdf2img'] + options + [input_name, self.output_form]
        with pdfprocess.Stdout() as stdout:
            process_code = subprocess.call(args, stdout=stdout)
            if process_code:
                # TODO: override default status_code
                return self.abort(process_code, self._get_errors(stdout))
        with open(output_file.name, 'rb') as image_file:
            image = base64.b64encode(image_file.read())
            return self.response(200, process_code=0, output=image)
    def _get_output_form(self):
        result = self.request_form.get('outputForm', 'tif').lower()
        if result == 'jpeg': result = 'jpg'
        if result == 'tiff': result = 'tif'
        return result
    def _pdf2img(self):
        with tempfile.NamedTemporaryFile() as input_file:
            self.input.save(input_file)
            input_file.flush()
            input_name = input_file.name
            pages, output_form = (self.pages, self.output_form)
            with OutputFile(input_name, pages, output_form) as output_file:
                return self._get_image(input_name, output_file)
    @classmethod
    def _get_errors(cls, stdout):
        error_prefix = 'ERROR: '
        lines = str(stdout).split('\n')
        errors = [line for line in lines if line.startswith(error_prefix)]
        return '\n'.join([error[len(error_prefix):] for error in errors])
    @property
    def input_name(self): return self._input_name
    @property
    def multipage_request(self): return '-' in self.pages or ',' in self.pages
    @property
    def output_form(self): return self._output_form
    @property
    def pages(self): return self._pages
    @property
    def tif_request(self): return self.output_form == 'tif'

