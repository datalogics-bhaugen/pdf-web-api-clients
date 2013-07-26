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

These packages depend on other packages (of course).

## Build

We use Buildout, which is a two-step process. These steps are executed by the Makefile's `build` (default) target:

* The repository is initialized by a bootstrap script that must be compatible with the version of Buildout we use (currently 2.2).
* Buildout uses its configuration to download packages, etc.

`BUILD` identifies the versions of the packages installed by Buildout. (Package dependencies are *not* version-specific.)

## Run

We use Supervisor to control the Gunicorn process that runs our Flask application.

* `bin/supervisord` starts the Supervisor daemon.
* `bin/supervisorctl` controls the Supervisor daemon.

## Test

To facilitate testing, there are scripts in `src/pdfprocess` that may be used to start the server without Supervisor. In this mode, the server creates its log in the current working directory instead of `var/log`.

PYTHONPATH might not work, but `bin/python` should.
