# web-api

Internet-accessible PDF API, formally known as "PDF WebAPI".

## Major Dependencies

Mac (different versions) is the primary development platform, and Ubuntu is the target deployment platform.

* [3scale](http://3scale.net)
* [Doxygen](http://www.stack.nl/~dimitri/doxygen/)
* [Flask](http://flask.pocoo.org)
* [Gunicorn](http://gunicorn.org)
* [PDF2IMG](http://www.datalogics.com/products/pdf2img/)
* [Python 2.7](https://www.python.org)

## Setup

### PDF2IMG

pdf2img must be in the PATH used by _pdfprocess_. Copy the latest version from `//ivy/raid/products/pdf2img/latest/`.

### Linux

These packages are required:

* make
* flex
* bison
* g++
* python-dev
* for lxml on Ubuntu
    * libxml2-dev
    * libxslt-dev

Copy PDF2IMG resources (e.g. pdf2img-resource-20130807.tar.gz) from `//ivy/raid/products/pdf2img` and install them in `/opt/pdfprocess/Resource/`.

For release builds, clone this repository into `/opt/pdfprocess`:

* To get the password for _pdfprocess_, send mail to pdfprocess@datalogics.com
* The pass phrase for the web-api deploy key is the password in lower case

### Mac

Xcode's Command Line Tools are required.

To install PDF2IMG:

* Open the disk image
* Drag the PDF2IMG directory to your home directory
    * Do not use _cp_ to copy the files!
* Ensure that ~/PDF2IMG/application/pdf2img is in your PATH
    * If ~/bin is in your PATH, add a link there

## Build

The Makefile's _build_ target (default) downloads packages, updates the files that record these dependencies, creates many files, and runs code quality tests.

    NB: Don't panic if it seems to stall. (It does this while building lxml.)

1. Documentation -- the build begins by generating HTML pages for our sample clients.

    * We clone the doxygen repository, build it, and use it to generate HTML for our sample PHP and Python clients.

2. Bootstrap -- the repository is initialized by a script that must be compatible with the version of Buildout we use (currently 2.2).

3. Buildout -- the buildout script uses its configuration to download and install packages. In some cases, this includes creating binaries from source code.

4. Dependencies -- the build updates the files that record third-party dependencies. Changes may be discovered by building the _status_ target.

5. Code Quality -- the build uses flake8 to check Python code quality.

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
* `test/test_client.py` runs `samples/python/pdfprocess.py` with test settings

## Issues

* API options differ from the ones offered by PDF2IMG, so the Flask application has a significant amount of option translation code.
* The _server_ namespace implements utilities on behalf of its _pdf2img_ package, e.g. a logger module. This introduces circular dependencies that should be removed.
