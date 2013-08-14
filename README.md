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

We use Buildout, which is a three-step process. These steps are executed by the Makefile's `build` (default) target:

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
    * To get the password for pdfprocess (to run sudo), send mail to `pdfprocess@datalogics.com`.
* `make`

## Linux Installation

* Configure nginx by editing /etc/nginx/sites-available/default
    * Uncomment the last server section
    * Change the root
        * root /usr/share/nginx/www;
    * Set SSL options
        * ssl_certificate /etc/nginx/ssl/server-test.crt;
        * ssl_certificate_key /etc/nginx/ssl/server-test.key;
        * ssl_verify_depth 3;
    * If the SSL key is missing, copy the appropriate one from //zeus/raid1/proj/procyon/web-api/etc/nginx/ssl
* On _pdfprocess_, `sudo make install-production` (this corrects the certificate and key names)
* On _pdfprocess-test_, `sudo make install-test`
* `bin/supervisord`
* `bin/supervisorctl status`
* If you are unfamiliar with /etc/init.d/nginx, run it without arguments
* `/etc/init.d/nginx restart`

## PDF2IMG

This application and its associated resources must be installed manually from archives stored at `//zeus/raid1/prducts/pdf2img/`.

* See [PDF2IMG](http://www.datalogics.com/pdf/doc/pdf2img.pdf) for platform-specific instructions
* For Linux
    * Unpack the two archives (one for pdf2img, one for its resources)
    * Make a link to the pdf2img executable in your bin directory, e.g. /home/thulasi/bin
    * Make links to the resource folders in your pdf2img directory
    * Add the pdf2img directory to your LD_LIBRARY_PATH

## Run

We use Supervisor to control the Gunicorn process that runs our Flask application.

* `bin/supervisord` starts the Supervisor daemon, which runs our Flask application in a Gunicorn process
* `bin/supervisorctl` controls the Supervisor daemon

## Test

These scripts facilitate testing:

* `bin/pdfprocess` runs our Flask application with its development server (Werkzeug)
* `samples/pdf2img.py` is a driver for our sample Python API client
* `scripts/gunicorn` runs our Flask application in a Gunicorn process
* `scripts/test_app.py` tests our Flask application directly
* `scripts/test_client.py` runs `samples/pdf2img.py` with test settings
* `scripts/test_server.py` uses test_client.py to test our server
* `bin/nose` runs regression tests in scripts/test_app.py and test_server.py

Common test procedures:
* The regression tests validate our Flask application
* If bin/supervisord fails to start Gunicorn, scripts/gunicorn might provide better diagnostic output
* To test the nginx configuration
    * /etc/init.d/nginx configtest
    * Run test_client.py from another host

## Paths

Our Flask application creates a log file in the directory specified by the LOG_PATH environment variable. If this is not defined, the application creates its log file in the current working directory.

`bin/pdfprocess` puts our eggs into the import path and sets LOG_PATH to `var/log`.

