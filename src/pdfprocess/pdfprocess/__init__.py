'API server'

import base64
import json
import subprocess
import tempfile

import flask

import api_flask
from api_tempfile import OutputFile, Stdout


def authorize(request_form):
    # TODO: use 3scale
    api_key = request_form.get('apiKey', None)
    return api_key == 'f54ab5d8-5775-42c7-b888-f074ba892b57'

def authorize_error(request_form):
    pass # TODO: set code, etc.

def get_image(options, input_file_storage, pages, output_form):
    if not pages and output_form.lower() == 'tif':
        options['multipage'] = True
    with tempfile.NamedTemporaryFile() as input_file:
        input_file_storage.save(input_file)
        input_file.flush()
        with OutputFile(input_file.name, pages, output_form) as output_file:
            return pdf2img(options, input_file, output_file, output_form)

def get_options(request_form):
    options = []
    for key, value in request_form.iteritems():
        if key not in ('apiKey', 'inputFile', 'outputForm'):
            key = '-' + key
            options.append(key if value == 'True' else '%s=%s' % (key, value))
    return options

def log_request(request_form, options, output_form):
    options = ' '.join(options)
    if options: options = ' ' + options
    input_file = request_form.get('inputFile', '<anon>')
    app.logger.info('pdf2img%s %s %s' % (options, input_file, output_form))

def pdf2img(options, input_file, output_file, output_form):
    options += output_file.options
    args = ['pdf2img'] + options + [input_file.name, output_form]
    with Stdout() as stdout:
        exit_code = subprocess.call(args, stdout=stdout)
        if exit_code: pdf2img_error(exit_code, str(stdout))
    with open(output_file.name, 'rb') as image_file:
        return flask.jsonify(image=base64.b64encode(image_file.read()))

def pdf2img_error(exit_code, stdout):
    flask.g.error = exit_code
    error_prefix = 'ERROR: '
    lines = stdout.split('\n')
    errors = [line for line in lines if line.startswith(error_prefix)]
    flask.g.text = '\n'.join([error[len(error_prefix):] for error in errors])
    flask.abort(500) # TODO: return different codes, etc.

app = api_flask.Application(__name__)

@app.before_first_request
def initialize():
    app.logger.info('%s started' % app.name)

@app.errorhandler(423)
def resource_locked(error):
    # TODO: if 'password' in request_form: ...
    return flask.jsonify(error=flask.g.error, 
        text='PDF Document Password incorrect or not given'), 423

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('%s: %s' % (flask.g.error, flask.g.text))
    return flask.jsonify(error=flask.g.error, text=flask.g.text), 500

@app.route('/0/actions/image', methods=['POST'])
def image():
    request_form = flask.request.form
    options = get_options(request_form)
    output_form = request_form.get('outputForm', '')
    log_request(request_form, options, output_form)

    if not authorize(request_form):
        return authorize_error(request_form)

    input = flask.request.files['input']
    pages = request_form.get('pages', '')
    return get_image(options, input, pages, output_form)

