# web-api

Internet-accessible PDF API, a.k.a. "PDF Web API" and "pdfprocess".

## System Requirements

* PDF2IMG
* Python 2.7

MacOS (different versions) is the primary development platform, and Ubuntu is the target deployment platform.

## Major Dependencies

* [3scale](http://3scale.net)
* [Doxygen](http://www.stack.nl/~dimitri/doxygen/)
* [Flask](http://flask.pocoo.org)
* [Gunicorn](http://gunicorn.org)
* [Supervisor](http://supervisord.org)

## Install PDF2IMG

This application must be in the PATH used by pdfprocess. Install it and its associated resources from archives stored at //zeus/raid1/products/pdf2img/.

* For Linux
    * Extract the two archives (one for pdf2img, one for its resources)
    * In ~/bin (e.g. /home/pdfprocess/bin), make a link to the pdf2img executable
    * In ~/.profile, add the pdf2img directory to your LD_LIBRARY_PATH
    * TODO: the web application uses the --fontlist option [...]
* For Mac
    * Open the disk image
    * Drag the PDF2IMG directory to your home directory
        * Do not use _cp_ to copy the files!
    * In ~/bin, make a link to ~/PDF2IMG/application/pdf2img

## Build

We use Buildout, which is a three-step process. These steps are executed by the Makefile's _build_ (default) target:

1. Documentation -- the build begins by cloning the doxygen repository, building a local copy of doxygen, and generating HTML pages for the API.

2. Bootstrap -- the repository is initialized by a script that must be compatible with the version of Buildout we use (currently 2.2).

3. Buildout -- the buildout script uses its configuration to download packages, etc.

* These packages must be installed on your system
    * make
    * flex
    * bison
    * g++
    * python-dev
    * sendmail (for Supervisor)
    * for lxml on Ubuntu
        * libxml2-dev
        * libxslt-dev
* Clone the web-api repository into /home/pdfprocess
    * To get the password for pdfprocess, send mail to pdfprocess@datalogics.com.
    * This password is also the pass phrase for the web-api deploy key.
* make _build_

## Run

We use Supervisor to control the Gunicorn server that runs our Flask application.

* `bin/supervisord` starts the Supervisor daemon, which runs our Flask application in a Gunicorn process
* `bin/supervisorctl` controls the Supervisor daemon

## Test

These scripts facilitate testing:

* `bin/pdfprocess` runs our Flask application with its development server (Werkzeug)
* `samples/pdf2img.py` is a driver for our sample Python API client
* `scripts/gunicorn` runs our Flask application in a Gunicorn process
* `test/test_client.py` runs `samples/pdf2img.py` with test settings
* `test/app_test.py` tests our Flask application directly
* `bin/nose` runs regression tests

Common test procedures:
* The regression tests validate our Flask application
* If bin/supervisord fails to start Gunicorn, scripts/gunicorn might provide better diagnostic output

## Logging

Our Flask application creates a log file in the directory specified by the LOG_PATH environment variable. If this is not defined, the application creates its log file in the current working directory.

`scripts\configure_logger.py` defines LOG_PATH to our var/log directory, and configures the logger to use UTC timestamps.
