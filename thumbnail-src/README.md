# web-api/thumbnail

This thumbnail server translates GET requests to POST requests as follows:

* enforces usage limits
* adds application ID and key
* adds default image size (max=250), if necessary
* returns web-api response, unchanged

## Build

* The Makefile uses web-api's buildout infrastructure

## Run

* `scripts/gunicorn` runs this server

## Test

These scripts facilitate testing:

* `bin/nose` runs the regression tests that validate this Flask application
* `bin/thumbnail` runs this Flask application with its development server (Werkzeug)
* `test/thumbnail_test.py` tests this server

