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

## Build

We use Buildout, which is a three-step process. These steps are executed by the Makefile's _build_ (default) target:

1. Documentation -- the build begins by cloning the doxygen repository, building a local copy of doxygen, and generating HTML pages for the API.

2. Bootstrap -- the repository is initialized by a script that must be compatible with the version of Buildout we use (currently 2.2).

3. Buildout -- the buildout script uses its configuration to download packages, etc.

* To support this build, these packages must be installed on your system
    * make
    * flex
    * bison
    * g++
    * python-dev
    * Python bindings for libxml2 (for ThreeScalePY)
        * Ubuntu: python-libxml2
        * Red Hat: libxml2-python
* Clone the repository into /home/pdfprocess if you are deploying the server
    * To get the password for pdfprocess (to run sudo), send mail to pdfprocess@datalogics.com.
* make _build_

## Linux Installation

* If there is no SSL key in /etc/nginx/ssl, copy the appropriate one from //zeus/raid1/proj/procyon/web-api/etc/nginx/ssl
* If an older version is installed, we recommend that you uninstall it, e.g. `sudo make uninstall-test`
* On _pdfprocess_, `sudo make install-production`
* On _pdfprocess-test_, `sudo make install-test`
* `bin/supervisord`
* `bin/supervisorctl status`
* If you are unfamiliar with /etc/init.d/nginx, run it without arguments
* `/etc/init.d/nginx restart`

## PDF2IMG

This application and its associated resources must be installed manually from archives stored at //zeus/raid1/products/pdf2img/.

* See [PDF2IMG](http://www.datalogics.com/pdf/doc/pdf2img.pdf) for platform-specific instructions
* For Linux
    * Extract the two archives (one for pdf2img, one for its resources)
    * In your bin directory (e.g. /home/pdfprocess/bin), make a link to the pdf2img executable
    * In your pdf2img directory, make links to the Resource directories
    * In .profile, add the pdf2img directory to your LD_LIBRARY_PATH

## Run

We use Supervisor to control the Gunicorn server that runs our Flask application.

* `bin/supervisord` starts the Supervisor daemon, which runs our Flask application in a Gunicorn process
* `bin/supervisorctl` controls the Supervisor daemon

## Test

These scripts facilitate testing:

* `bin/pdfprocess` runs our Flask application with its development server (Werkzeug)
* `samples/pdf2img.py` is a driver for our sample Python API client
* `scripts/gunicorn` runs our Flask application in a Gunicorn process
* `test/test_app.py` tests our Flask application directly
* `test/test_client.py` runs `samples/pdf2img.py` with test settings
* `bin/nose` runs regression tests in test
    * test_3scale.py
    * test_options.py
    * test_server.py

Common test procedures:
* The regression tests validate our Flask application
* If bin/supervisord fails to start Gunicorn, scripts/gunicorn might provide better diagnostic output
* To test the nginx configuration
    * /etc/init.d/nginx configtest
    * Run test_client.py from another host

## Logging

Our Flask application creates a log file in the directory specified by the LOG_PATH environment variable. If this is not defined, the application creates its log file in the current working directory.

`scripts\configure_logger.py` defines LOG_PATH to our var/log directory, and configures the logger to use UTC timestamps.
