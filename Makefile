DOXYGEN_CLEAN = rm -rf *.css *.html *.js *.png search
ERASE = printf '' >
GIT_HOOK = .git/hooks/pre-commit
MAKE_THUMBNAIL = make --directory thumbnail-src
PHPDOC = doc/php/index.html
PLATFORM = $(shell uname -s)
PYDOC = doc/python/index.html
QA = bin/flake8 --max-complexity 10
REPLACE_KEY = test/scripts/replace_key
TEST_PDFPROCESS = test/pdfprocess
VENV = eggs/virtualenv-*.egg/virtualenv.py

VAR_LOG = var/log
LOG_NAME = pdfprocess.log
APP_LOG = $(VAR_LOG)/$(LOG_NAME)
SERVER_LOG = $(VAR_LOG)/server
AUX_LOG = $(SERVER_LOG)/$(LOG_NAME)

build: $(GIT_HOOK) $(APP_LOG) $(AUX_LOG) Resource eggs tmp venv html
ifeq ($(PLATFORM), Darwin)
	$(ERASE) versions.cfg
endif
	venv/bin/python bootstrap.py
	scripts/make_server_cfg > cfg/versions
	bin/buildout | scripts/make_versions_cfg > versions.cfg
	@diff $(VENV) virtualenv.py > /dev/null || echo Upgrade virtualenv!
	@cp $(VENV) .
	@$(MAKE_THUMBNAIL)
	@make qa test-scripts bin/segfault

clean: html-clean
	rm -rf .installed.cfg $(GIT_HOOK) bin develop-eggs parts venv
	$(ERASE) $(APP_LOG); $(ERASE) $(AUX_LOG)
	rm -rf $(TEST_PDFPROCESS) test/*.png
	@$(MAKE_THUMBNAIL) $@

qa:
	$(QA) cfg samples scripts src test
	@$(MAKE_THUMBNAIL) $@

status:
	@git status | grep 'nothing to commit' > /dev/null

test-scripts: $(TEST_PDFPROCESS)
	$(REPLACE_KEY) samples/perl/pdfprocess.pl > $^/perl
	$(REPLACE_KEY) samples/php/pdfprocess.php > $^/php
	$(REPLACE_KEY) samples/python/pdfprocess.py > $^/python
	chmod +x $^/*
	cp samples/*/pdfclient.* $^

html: $(PHPDOC) $(PYDOC)

html-clean: phpdoc-clean pydoc-clean

phpdoc-clean:
	cd doc/php; $(DOXYGEN_CLEAN)

pydoc-clean:
	cd doc/python; $(DOXYGEN_CLEAN)

.PHONY: build clean qa status test-scripts
.PHONY: html html-clean phpdoc-clean pydoc-clean

$(APP_LOG): $(VAR_LOG)
	touch $@

$(AUX_LOG): $(SERVER_LOG)
	touch $@

$(GIT_HOOK): scripts/pre-commit
	ln -s ../../$^ $@

$(PHPDOC): doxygen samples/php/*
	@make phpdoc-clean
	doxygen/bin/doxygen samples/php/Doxyfile

$(PYDOC): doxygen samples/python/*
	@make pydoc-clean
	doxygen/bin/doxygen samples/python/Doxyfile

bin/segfault: test/src/segfault.c
	gcc $^ -o $@

Resource:
ifeq ($(PLATFORM), Linux)
	ls -d /opt/pdfprocess/$@/CMap
endif

doxygen:
	git clone https://github.com/doxygen/$@.git
	cd $@; ./configure; make

eggs tmp $(TEST_PDFPROCESS) $(VAR_LOG) $(SERVER_LOG):
	mkdir -p $@

venv:
	python virtualenv.py --no-setuptools $@
