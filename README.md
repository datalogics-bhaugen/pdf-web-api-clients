# web-api

Internet-accessible PDF API, formally known as "PDF WebAPI". This repository resembles [stopr](https://github.com/datalogics/stopr) in many ways.

Remember to look at our [Confluence](https://wiki.datalogics.com/display/EN/PDF+Web+API) page!

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

pdf2img must be in the PATH used by the service account. Copy the latest version from `//ivy/raid/products/pdf2img/latest/`.

### Linux

These packages are required:

* make
* flex
* bison
* g++
* python-dev
* for Scout on Ubuntu
    * libmagic-dev
* for lxml on Ubuntu
    * libxml2-dev
    * libxslt-dev
    * zlib1g-dev
* for thumbnail server usage limit enforcement on Ubuntu
    * sqlite

#### Cloud

Our [Confluence](https://wiki.datalogics.com/display/EN/PDF+Web+API) page describes how to build this repository on our cloud build server. This server is also the host for our test environment. For more information about our services, please read that page!

### Mac

Xcode's Command Line Tools are required.

To install PDF2IMG:

* Open the disk image
* Drag the PDF2IMG directory to your home directory
    * Do not use _cp_ to copy the files!
* Ensure that ~/PDF2IMG/application/pdf2img is in your PATH
    * If ~/bin is in your PATH, add a link there

## Build

The Makefile's _all_ target (default) downloads packages, updates the files that record these dependencies, creates many files, and runs code quality tests.

To avoid unsolved build issues on Mac 10.9 (Mavericks), use the _app_ target instead.

    NB: Don't panic if the build seems to stall. (It does this while building lxml.)

1. Bootstrap -- the repository is initialized by a script that must be compatible with the version of Buildout we use (currently 2.2).

2. Buildout -- the buildout script uses its configuration to download and install packages. In some cases, this includes creating binaries from source code.

    NB: On some older Linux hosts, buildout fails unless you add `check_certificate=off` to your wget configuration (~/.wgetrc).

3. Code Quality -- the build uses flake8 to check Python code quality.

### Dependency Management

web-api and [stopr](https://github.com/datalogics/stopr) use different approaches to handling third-party dependencies. For the most part, web-api does not specify third-party package versions. Instead, the build updates a file that tracks these dependencies so we can discover when they change. The daily build automatically tests these upgrades, so we can accept them as they are released.

To use specific versions of third-party packages, edit the _pinned-versions_ section in `base.cfg`.

## Run

* `scripts/gunicorn` starts this server
* `thumbnail/scripts/gunicorn` runs the thumbnail server

    NB: To run multiple servers on one host, edit the port specifications in the generated server configuration (cfg/server).

## Test

These scripts facilitate testing:

* `bin/nose` runs the regression tests that validate this server's Flask application
* `bin/server` runs this Flask application with its development server (Werkzeug)
* `test/app_test.py` tests this server's Flask application directly
* `test/test_client.py` runs `samples/python/pdfprocess.py` with valid 3scale credentials

Testing with gunicorn is possible (of course), but it's less convenient.

## Documentation

The Makefile's _html_ target generates HTML pages:

* We clone the doxygen repository, build it, and use it to generate HTML for our sample PHP and Python clients.
* We download and install Sphinx, and use it to generate HTML for this server's Flask application.

## Issues

* API options differ from the ones offered by PDF2IMG, so the Flask application has a significant amount of option translation code.
* The _server_ namespace implements utilities on behalf of its _pdf2img_ package, e.g. a logger module. This introduces circular dependencies that should be removed.
* The _server_ namespace attempts to create a framework that provides generic HTTP request functionality and supports using backend applications to process requests. _server.pdf2img_ is supposed to be the RenderPages plugin for this framework. As is often the case when there is only one plugin, the division of labor between it and the framework is probably wrong. 
