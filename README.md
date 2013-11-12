# web-api

Internet-accessible PDF API, formally known as "PDF WebAPI".

## System Requirements

* PDF2IMG
* Python 2.7
* `pdfprocess` login

MacOS (different versions) is the primary development platform, and Ubuntu is the target deployment platform.

## Major Dependencies

* [3scale](http://3scale.net)
* [Doxygen](http://www.stack.nl/~dimitri/doxygen/)
* [Flask](http://flask.pocoo.org)
* [Gunicorn](http://gunicorn.org)

## Install PDF2IMG

This application must be in the PATH used by pdfprocess. Install it and its associated resources from archives stored at //ivy/raid/products/pdf2img/.

* For Linux
    * The server image includes this application
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

* For Linux, these packages must be installed
    * make
    * flex
    * bison
    * g++
    * python-dev
    * for lxml on Ubuntu
        * libxml2-dev
        * libxslt-dev
* For Mac, Xcode's Command Line Tools must be installed
* Clone the web-api repository into /home/pdfprocess
    * To get the password for pdfprocess, send mail to pdfprocess@datalogics.com
    * The pass phrase for the web-api deploy key is the password in lower case
* make _build_

## Run

* `scripts/gunicorn` starts this server
* `thumbnail/scripts/gunicorn` runs the thumbnail server

On Linux, the corresponding init daemon commands are:

* `/sbin/start webapi` and `/sbin/stop webapi`
* `/sbin/start thumbnail` and `/sbin/stop thumbnail`

## Monitor

* `web-api/monitor.py` is used by Scout to monitor this server
* `web-api/monitor-thumbnail.py` is used to monitor the thumbnail server

## Test

These scripts facilitate testing:

* `bin/nose` runs the regression tests that validate this Flask application
* `bin/server` runs this Flask application with its development server (Werkzeug)
* `test/app_test.py` tests this Flask application directly
* `test/test_client.py` runs `samples/pdfprocess.py` with test settings

## Issues

* API options differ from the ones offered by PDF2IMG, so the Flask application has a significant amount of option translation code.
* The base Action class handles features supported by all requests, whereas the pdf2img.Action subclass handles features specific to PDF2IMG requests. The boundary between these classes probably needs refactoring.
* The _server_ namespace implements utilities on behalf of its pdf2img package, e.g. a logger module. This introduces circular dependencies that should be removed.
