ERASE = printf '' >
GIT_HOOK = .git/hooks/pre-commit
MAKE_THUMBNAIL = make --directory thumbnail-src
PHP_DOCUMENTOR = bin/phpDocumentor.phar
PHPDOC = doc/php
PLATFORM = $(shell uname -s)
PYDOC = doc/python/index.html
QA = bin/flake8 --max-complexity 10
VENV = eggs/virtualenv-*.egg/virtualenv.py

VAR_LOG = var/log
LOG_NAME = pdfprocess.log
APP_LOG = $(VAR_LOG)/$(LOG_NAME)
SERVER_LOG = $(VAR_LOG)/server
AUX_LOG = $(SERVER_LOG)/$(LOG_NAME)

build: $(GIT_HOOK) $(APP_LOG) $(AUX_LOG) Resource eggs tmp venv html
ifeq ($(PLATFORM), Darwin)
	# $(ERASE) versions.cfg
endif
	venv/bin/python bootstrap.py
	scripts/make_server_cfg > cfg/versions
	bin/buildout # | scripts/make_versions_cfg > versions.cfg
	@diff $(VENV) virtualenv.py > /dev/null || echo Upgrade virtualenv!
	@cp $(VENV) .
	@$(MAKE_THUMBNAIL)
	@make qa

clean: pydoc-clean
	rm -rf .installed.cfg $(GIT_HOOK) bin develop-eggs parts venv
	$(ERASE) $(APP_LOG); $(ERASE) $(AUX_LOG)
	@$(MAKE_THUMBNAIL) $@

qa: bin/segfault
	$(QA) cfg samples scripts src test
	@$(MAKE_THUMBNAIL) $@

html: $(PHPDOC) $(PYDOC)

pydoc-clean:
	cd doc/python; rm -rf *.css *.html *.js *.png search

.PHONY: build clean qa html pydoc-clean

$(APP_LOG): $(VAR_LOG)
	touch $@

$(AUX_LOG): $(SERVER_LOG)
	touch $@

$(GIT_HOOK): scripts/pre-commit
	ln -s ../../$^ $@

Resource:
ifeq ($(PLATFORM), Linux)
	ls -d ../$@/CMap
endif

bin/segfault: test/src/segfault.c
	gcc $^ -o $@

bin eggs tmp $(VAR_LOG) $(SERVER_LOG):
	mkdir -p $@

doxygen:
	git clone https://github.com/doxygen/$@.git
	cd $@; ./configure; make

venv:
	python virtualenv.py $@

$(PHP_DOCUMENTOR):
	@make bin
	curl --output $@ http://phpdoc.org/$(@F)

$(PHPDOC): $(PHP_DOCUMENTOR) samples/php/*
	@rm -rf doc/php
	php $< -d samples/php -t $@ --force

$(PYDOC): doxygen samples/python/*
	doxygen/bin/doxygen samples/python/Doxyfile
