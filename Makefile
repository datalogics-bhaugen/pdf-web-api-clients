ERASE = printf '' >
GIT_HOOK = .git/hooks/pre-commit
MAKE_HTML = make --directory doc
MAKE_THUMBNAIL = make --directory thumbnail-src
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

build: $(GIT_HOOK) $(APP_LOG) $(AUX_LOG) Resource cfg/server eggs tmp venv
	venv/bin/python bootstrap.py
	bin/buildout | scripts/make_versions_cfg > versions.cfg
	@cp $(VENV) .
	@$(MAKE_THUMBNAIL)
	@make qa test-scripts bin/segfault

clean:
	rm -rf .installed.cfg $(GIT_HOOK) bin develop-eggs parts venv
	$(ERASE) $(APP_LOG); $(ERASE) $(AUX_LOG)
	rm -rf $(TEST_PDFPROCESS) test/*.png
	@$(MAKE_THUMBNAIL) $@

html:
	@$(MAKE_HTML)

qa:
	$(QA) cfg samples scripts src test
	@$(MAKE_THUMBNAIL) $@

test-scripts: $(TEST_PDFPROCESS)
	$(REPLACE_KEY) samples/php/pdfprocess.php > $^/php
	$(REPLACE_KEY) samples/python/pdfprocess.py > $^/python
	chmod +x $^/*
	cp samples/*/pdfclient.* $^

.PHONY: build clean html qa test-scripts

$(APP_LOG): $(VAR_LOG)
	touch $@

$(AUX_LOG): $(SERVER_LOG)
	touch $@

$(GIT_HOOK): scripts/pre-commit
	ln -s ../../$^ $@

Resource:
ifeq ($(PLATFORM), Linux)
	ls -d /opt/pdfprocess/$@/CMap
endif

bin/segfault: test/src/segfault.c
	gcc $^ -o $@

cfg/server:
	scripts/make_server_cfg > $@

eggs tmp $(TEST_PDFPROCESS) $(VAR_LOG) $(SERVER_LOG):
	mkdir -p $@

venv:
	python virtualenv.py --no-setuptools $@
