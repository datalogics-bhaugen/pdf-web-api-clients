BOOTSTRAP = venv/bin/python bootstrap.py
BUILDOUT = bin/buildout
ERASE = printf '' >
GIT_HOOK = .git/hooks/pre-commit
MAKE_HTML = make --directory doc
MAKE_THUMBNAIL = make --directory thumbnail
PLATFORM = $(shell uname -s)
QA = bin/flake8 --max-complexity 10
REPLACE_KEY = test/scripts/replace_key
TEST_PDFPROCESS = test/pdfprocess
VENV = eggs/virtualenv-*.egg/virtualenv.py

VAR_LOG = var/log
LOG_NAME = pdfprocess.log
APP_LOG = $(VAR_LOG)/$(LOG_NAME)
SERVER_LOG = $(VAR_LOG)/server
AUX_LOG = $(SERVER_LOG)/$(LOG_NAME)

all: $(AUX_LOG) $(BOOTSTRAP) resource-test
	$(BOOTSTRAP)
	$(BUILDOUT) | scripts/make_versions_cfg > versions.cfg
	@$(MAKE_THUMBNAIL) $@
	@make files qa

app: $(BOOTSTRAP)
	$(BOOTSTRAP) -c base.cfg
	$(BUILDOUT) -c base.cfg
	@make files qa

clean:
	rm -rf .installed.cfg $(GIT_HOOK) bin develop-eggs parts venv
	$(ERASE) $(APP_LOG); $(ERASE) $(AUX_LOG)
	rm -rf $(TEST_PDFPROCESS)
	rm -f test/*.bmp test/*.gif test/*.jpg test/*.png test/*.tif
	@$(MAKE_THUMBNAIL) $@

files: $(GIT_HOOK) $(APP_LOG) cfg/server eggs tmp
	@cp $(VENV) .
	@make test-scripts bin/segfault

html:
	@$(MAKE_HTML)

qa:
	$(QA) cfg samples scripts src test

resource-test:
ifeq ($(PLATFORM), Linux)
	ls -d /opt/pdfprocess/Resource/CMap
endif

test-scripts: $(TEST_PDFPROCESS)
	$(REPLACE_KEY) samples/php/pdfprocess.php > $^/php
	$(REPLACE_KEY) samples/python/pdfprocess.py > $^/python
	chmod +x $^/*
	cp samples/*/pdfclient.* $^

.PHONY: all app clean files html qa resource-test test-scripts

$(APP_LOG): $(VAR_LOG)
	touch $@

$(AUX_LOG): $(SERVER_LOG)
	touch $@

$(BOOTSTRAP): venv

$(GIT_HOOK): scripts/pre-commit
	ln -s ../../$^ $@

bin/segfault: test/src/segfault.c
	gcc $^ -o $@

cfg/server: scripts/make_server_cfg
	$^ > $@

eggs tmp $(TEST_PDFPROCESS) $(VAR_LOG) $(SERVER_LOG):
	mkdir -p $@

venv:
	python virtualenv.py --no-setuptools $@
