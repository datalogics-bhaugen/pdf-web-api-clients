# web-api/thumbnail

The thumbnail server translates GET requests to POST requests as follows:

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
* `bin/server` runs this Flask application with its development server (Werkzeug)
* `test/server_test.py` tests this server

## Usage Limits

The thumbnail server uses the 3scale API to retrieve the usage limits for WebAPI's public plan. Usage statistics are stored on a per-server basis in a SQLite database. This should be copied from a prod server to the build server before creating a new server image.
