# web-api/thumbnail

This thumbnail server translates GET requests to POST requests as follows:

* adds application ID and key (Joel's credentials)
* adds default image size (max=150), if necessary
* returns web-api response, unchanged

## Build

* The Makefile uses web-api's buildout infrastructure

## Run

* `scripts/gunicorn` runs this server
* `scripts/monitor.py` is used by Scout to monitor this server

## Test

These scripts facilitate testing:

* `bin/nose` runs the regression tests that validate this Flask application
* `bin/thumbnail` runs this Flask application with its development server (Werkzeug)
* `test/thumbnail_test.py` tests this server

