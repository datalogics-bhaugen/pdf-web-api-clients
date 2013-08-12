# web-api

Internet-accessible PDF API, a.k.a. "PDF Web API" and "pdfprocess".

## System Requirements

* PDF2IMG
* Python 2.7
* nginx

MacOS (different versions) is the primary development platform, and Ubuntu is the target deployment platform.

## Major Dependencies

* Doxygen
* Flask
* Gunicorn
* Supervisor
* ThreeScalePY

## PDF2IMG

This application and its associated resources must be installed manually from archives stored at `//zeus/raid1/prducts/pdf2img/`.

* Install the application in your bin directory, e.g. /home/thulasi/bin/.
* See [PDF2IMG](http://www.datalogics.com/pdf/doc/pdf2img.pdf) for platform-specific instructions.

## Build

We use Buildout, which is a three-step process. These steps are executed by the Makefile's `build` (default) target:

1. Documentation -- the build begins by cloning the doxygen repository, building a local copy of doxygen, and generating HTML pages for the API.

2. Bootstrap -- the repository is initialized by a script that must be compatible with the version of Buildout we use (currently 2.2).

3. Buildout -- the buildout script uses its configuration to download packages, etc. `BUILD` identifies the versions of the packages installed by Buildout.

To support this build, these packages must be installed on your system:

* make
* flex
* bison
* g++
* python-dev
* Python bindings for libxml2 (for ThreeScalePY)

## Run

We use Supervisor to control the Gunicorn process that runs our Flask application.

* `bin/supervisord` starts the Supervisor daemon, which runs our Flask application in a Gunicorn process.
* `bin/supervisorctl` controls the Supervisor daemon.

## Test

These scripts facilitate testing:

* `bin/pdfprocess` runs our Flask application with its development server (Werkzeug).
* `samples/pdf2img.py` is a driver for our sample Python API client.
* `scripts/gunicorn` runs our Flask application in a Gunicorn process.
* `scripts/test_app.py` tests our Flask application directly.
* `scripts/test_client.py` runs `samples/pdf2img.py` with test settings.
* `scripts/test_server.py` uses test_client.py to test our server.
* `bin/nose` runs regression tests in scripts/test_app.py and test_server.py.

## Paths

Our Flask application creates a log file in the directory specified by the LOG_PATH environment variable. If this is not defined, the application creates its log file in the current working directory.

`bin/pdfprocess` puts our eggs into the import path and sets LOG_PATH to `var/log`.

