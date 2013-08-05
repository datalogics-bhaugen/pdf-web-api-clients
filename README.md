# web-api

Internet-accessible PDF API, a.k.a. "PDF Web API" and "pdfprocess".

## System Requirements

* PDF2IMG
* Python 2.7
* nginx

MacOS (different versions) is the primary development platform, and Ubuntu is the target deployment platform.

## Major Package Dependencies

* Flask
* Gunicorn
* Supervisor
* ThreeScalePY

These packages depend on other packages (of course).

## Build

We use Buildout, which is a two-step process. These steps are executed by the Makefile's `build` (default) target:

* The repository is initialized by a bootstrap script that must be compatible with the version of Buildout we use (currently 2.2).
* Buildout uses its configuration to download packages, etc.

`BUILD` identifies the versions of the packages installed by Buildout. (Package dependencies are *not* version-specific.)

We do not use Buildout to install doxygen or libxml2 (needed by ThreeScalePY). These are built/installed by their respective Makefile targets.

## Run

We use Supervisor to control the Gunicorn process that runs our Flask application.

* `bin/supervisord` starts the Supervisor daemon, which runs our Flask application in a Gunicorn process.
* `bin/supervisorctl` controls the Supervisor daemon.

## Test

These scripts facilitate testing each piece of the call stack:

* `bin/pdfprocess` runs our Flask application with its development server (Werkzeug).
* `scripts/gunicorn` runs our Flask application in a Gunicorn process.

## Paths

Our Flask application creates a log file in the directory specified by the LOG_PATH environment variable. If this is not defined, the application creates its log file in the current working directory.

`bin/pdfprocess` puts our eggs into the import path and sets LOG_PATH to `var/log`.

