#!/usr/bin/env python

'web api server'

import flask
import logging
import subprocess
import tempfile
from logging.handlers import TimedRotatingFileHandler

def authorize(request_form):
    # TODO: use 3scale
    api_key = request_form.get('apiKey', None)
    return api_key == 'f54ab5d8-5775-42c7-b888-f074ba892b57'

def authorize_error(request_form):
    pass # TODO: set code, etc.

def get_image(options, input_file_storage, output_form):
    with tempfile.NamedTemporaryFile() as input_file:
        input_file_storage.save(input_file)
        input_file.flush()
        args = ['pdf2img', '-output=TODO'] + options
        subprocess.call(args + [input_file.name, output_form])
        return flask.send_file('TODO_1.%s' % output_form)

def get_options(request_form):
    options = []
    for key, value in request_form.iteritems():
        if key not in ('apiKey', 'inputFile', 'outputForm'):
            options.append(key if value == 'True' else '%s:%s' % (key, value))
    return options

def log_request(request_form, options, output_form):
    options = ' '.join(options)
    if options: options = ' ' + options
    input_file = request_form.get('inputFile', '')
    app.logger.info('pdf2img%s %s %s' % (options, input_file, output_form))

def make_file_handler(name):
    rotate_daily = 'D'
    return TimedRotatingFileHandler('%s.log' % name, rotate_daily)

app = flask.Flask(__name__)
app.logger.addHandler(make_file_handler(app.name))
app.logger.setLevel(logging.INFO)
app.logger.info('%s started' % app.name)

@app.route('/0/actions/image', methods=['POST'])
def image():
    request_form = flask.request.form
    options = get_options(request_form)
    output_form = request_form.get('outputForm', '')
    log_request(request_form, options, output_form)

    if not authorize(request_form): return authorize_error(request_form)
    return get_image(options, flask.request.files['file'], output_form)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

