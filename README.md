# web-api

Internet-accessible PDF API, a.k.a. "PDF Web API" and "pdfprocess".

## System Requirements

* PDF2IMG
* Python 2.7
* nginx

MacOS (different versions) is the primary development platform, and Ubuntu is the target deployment platform.

## Major Dependencies

* [3scale](http://3scale.net)
* [Doxygen](http://www.stack.nl/~dimitri/doxygen/)
* [Flask](http://flask.pocoo.org)
* [Gunicorn](http://gunicorn.org)
* [Supervisor](http://supervisord.org)

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
* Clone the repository into /home/pdfprocess if you are deploying the server
    * To get the password for pdfprocess (to run sudo), send mail to pdfprocess@datalogics.com.
* make _build_

## Upgrade nginx

* /etc/init.d/nginx stop
* apt-get autoremove nginx
* apt-key add etc/nginx/nginx_signing.key
* Append the following to the end of /etc/apt/sources.list
    * deb http://nginx.org/packages/ubuntu/ precise nginx
    * deb-src http://nginx.org/packages/ubuntu/ precise nginx
    * (replace *precise* with the appropriate Ubuntu codename as needed)
* apt-get update
* apt-get install nginx
* If there is no SSL key in /etc/nginx/ssl, copy the appropriate one from //zeus/raid1/proj/procyon/web-api/etc/nginx/ssl

Near the bottom of /etc/nginx/nginx.conf, you should see this:

    include /etc/nginx/conf.d/*.conf;

If necessary, add this line immediately after it:

    include /etc/nginx/sites-enabled/*;

## Install pdfprocess

* If an older version is installed, we recommend that you uninstall it, e.g. `sudo make uninstall-test`
* On _pdfprocess_, `sudo make install-production`
* On _pdfprocess-test_, `sudo make install-test`
* `bin/supervisord`
* `bin/supervisorctl status`
* If you are unfamiliar with /etc/init.d/nginx, run it without arguments
* `/etc/init.d/nginx restart`

## Install PDF2IMG

Install this application and its associated resources from archives stored at //zeus/raid1/products/pdf2img/.

* For Linux
    * Extract the two archives (one for pdf2img, one for its resources)
    * In ~/bin directory (e.g. /home/pdfprocess/bin), make a link to the pdf2img executable
    * In your pdf2img directory, make links to the Resource directories
    * In ~/.profile, add the pdf2img directory to your LD_LIBRARY_PATH
* For Mac
    * Create ~/Frameworks for the framework directories
    * Copy the pdf2img executable to ~/bin
    * Ignore the resources

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
* `bin/nose` runs regression tests in test
    * 3scale_test.py
    * libxml2_test.py
    * options_test.py
    * server_test.py
    * syntax_test.py

Common test procedures:
* The regression tests validate our Flask application
* If bin/supervisord fails to start Gunicorn, scripts/gunicorn might provide better diagnostic output
* To test the nginx configuration
    * /etc/init.d/nginx configtest
    * Run test_client.py from another host

## Logging

Our Flask application creates a log file in the directory specified by the LOG_PATH environment variable. If this is not defined, the application creates its log file in the current working directory.

`scripts\configure_logger.py` defines LOG_PATH to our var/log directory, and configures the logger to use UTC timestamps.
