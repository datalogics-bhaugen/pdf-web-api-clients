"RenderPages request handler"

import os
import subprocess

import flask

import server
import options
import translator
import argument_parser
from server import Error, ErrorCode, logger
from output_file import OutputFile


class Action(server.Action):
    "uses pdf2img application to process requests"
    def __call__(self):
        self._parser = argument_parser.ArgumentParser()
        try:
            self._parser(self.options)
            self.input.initialize()
        except Error as error:
            self.raise_error(error)
        except Exception as exc:
            self.raise_error(Error(ErrorCode.InvalidSyntax, exc.message))
        self.client.authorize()
        return self._pdf2img()
    def _content_type(self):
        image_type = self.output_format.lower()
        if image_type == 'jpg': image_type = 'jpeg'
        if image_type == 'tif': image_type = 'tiff'
        return u'image/{}'.format(image_type)
    def _get_image(self, input_name, output_file):
        with server.Stdout() as stdout:
            if subprocess.call(self._pdf2img_args(input_name), stdout=stdout):
                self.raise_error(Action.get_error(stdout))
        with open(output_file.name, 'rb') as image_file:
            content_type = self._content_type()
            return flask.Response(image_file.read(), content_type=content_type)
    def _pdf2img(self):
        with server.TemporaryFile() as input_file:
            self.input.save(input_file)
            with OutputFile(input_file.name, self.output_format) as output:
                return self._get_image(input_file.name, output)
    def _pdf2img_args(self, input_name):
        result = ['pdf2img'] + Action._options() + self._parser.pdf2img_options
        if self.password: result += [u'-password={}'.format(self.password)]
        result += [input_name, self.output_format]
        logger.debug(' '.join(result))
        return result
    @classmethod
    def _options(cls):
        if not server.RESOURCE: return []
        resources = ('CMap', 'Font', 'Unicode')
        resources = [os.path.join(server.RESOURCE, r) for r in resources]
        return [u'-fontlist="{}"'.format(';'.join(resources))]
    @property
    def request_type(self): return 'RenderPages'
    @property
    def output_format(self): return self._parser.output_format
    @property
    def pages(self): return self._parser.pages
