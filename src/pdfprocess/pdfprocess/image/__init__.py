"pdfprocess image package"

import base64
import subprocess
import tempfile

import flask

import pdfprocess
from .argument_parser import ArgumentParser, Flag
from .output_file import OutputFile


class Action(pdfprocess.Action):
    def __init__(self, logger, request):
        pdfprocess.Action.__init__(self, logger, request)
        self._input_file = self.request_form.get('inputFile', '<anon>')
        self._output_form = self.request_form.get('outputForm', 'tif').lower()
        self._pages = self.request_form.get('pages', '')
        self._options = self._get_options()
    def __call__(self):
        self._log_request()
        try:
            argument_parser = ArgumentParser()
            argument_parser(self._options + ['input', self.output_form])
        except Exception as exc:
            return self.abort(-1, exc.message) # TODO: process_code
        if self.multipage_request and not self.tif_request:
            return self.abort(666, 'TODO: bad multipage request')
        return self._pdf2img() if self.authorize() else self.authorize_error()
    def _get_image(self, input, output_file):
        # TODO: translate height/width to pixelcount
        options = self._options + output_file.options
        args = ['pdf2img'] + options + [input, self.output_form]
        with pdfprocess.Stdout() as stdout:
            process_code = subprocess.call(args, stdout=stdout)
            if process_code:
                # TODO: override default status_code
                return self.abort(process_code, self._get_errors(stdout))
        with open(output_file.name, 'rb') as image_file:
            image = base64.b64encode(image_file.read())
            return flask.jsonify(processCode=0, image=image)
    def _get_options(self):
        result = []
        options = ArgumentParser.options()
        for key, value in self.request_form.iteritems():
            if key in options:
                option = options[options.index(key)]
                if not isinstance(option, Flag):
                    result.append('%s=%s' % (option.name, value))
                elif value:
                    result.append(option.name)
        return result
    def _log_request(self):
        options = ' '.join(self._options)
        if options: options = ' ' + options
        input_file = self.input_file
        if ' ' in input_file: input_file = '"%s"' % input_file
        self.logger.info('pdf2img%s %s %s' %
            (options, input_file, self.output_form))
    def _pdf2img(self):
        with tempfile.NamedTemporaryFile() as input_file:
            self.input.save(input_file)
            input_file.flush()
            input = input_file.name
            pages = self.pages
            with OutputFile(input, pages, self.output_form) as output_file:
                return self._get_image(input, output_file)
    @classmethod
    def _get_errors(cls, stdout):
        error_prefix = 'ERROR: '
        lines = str(stdout).split('\n')
        errors = [line for line in lines if line.startswith(error_prefix)]
        return '\n'.join([error[len(error_prefix):] for error in errors])
    @property
    def input_file(self): return self._input_file
    @property
    def multipage_request(self): return '-' in self.pages or ',' in self.pages
    @property
    def output_form(self): return self._output_form
    @property
    def pages(self): return self._pages
    @property
    def tif_request(self): return self.output_form == 'tif'

