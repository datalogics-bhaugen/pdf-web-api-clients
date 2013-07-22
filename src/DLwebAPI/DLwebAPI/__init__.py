#!/usr/bin/env python

'web api server'

import flask
import logging
import subprocess
from logging.handlers import TimedRotatingFileHandler

def authenticate(request_form):
    # TODO: use 3scale
    api_key = request_form.get('apiKey', None)
    return api_key == 'f54ab5d8-5775-42c7-b888-f074ba892b57'

def get_options(request_form):
    options = []
    for arg, value in request_form.iteritems():
        if arg not in ('apiKey', 'inputFile', 'outputForm'):
            options.append(arg)
            if value != 'True': options.append(value)
    return options

def log_request(options, request_form):
    options = ' '.join(options)
    if options: options = ' ' + options
    input_file = request_form.get('inputFile', '')
    output_form = request_form.get('outputForm', '')
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
    options = get_options(flask.request.form)
    log_request(options, flask.request.form)
    if authenticate(flask.request.form):
        # TODO: use tempfile module and 'with' syntax
        input_file = flask.request.form.get('inputFile', '')
        output_form = flask.request.form.get('outputForm', '')
        subprocess.call(["pdf2img", input_file, output_form])
        if input_file.endswith(".pdf"):
            input_file = input_file[:-len(".pdf")]
        output_file = (input_file + "_1." + output_form)
        return flask.send_file(output_file)
    # TODO: return error

if __name__ == '__main__':
    app.run(host='0.0.0.0')

