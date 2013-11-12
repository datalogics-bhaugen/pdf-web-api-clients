DOXYGEN = doc/html/index.html
ERASE = printf '' >
GIT_HOOK = .git/hooks/pre-commit
QA = bin/flake8 --max-complexity 10
MAKE_THUMBNAIL = make --directory thumbnail-src
PLATFORM = $(shell uname -s)
VAR_LOG = var/log
VENV = eggs/virtualenv-*.egg/virtualenv.py

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

clean: html-clean
	rm -rf .installed.cfg $(GIT_HOOK) bin develop-eggs parts venv
	$(ERASE) $(APP_LOG); $(ERASE) $(AUX_LOG)
	@$(MAKE_THUMBNAIL) clean

qa: bin/segfault
	$(QA) cfg samples scripts src test
	@$(MAKE_THUMBNAIL) qa

html: $(DOXYGEN)

html-clean:
	cd doc/html; rm -rf *.css *.html *.js *.png search

.PHONY: build clean qa html html-clean

$(APP_LOG): $(VAR_LOG)
	touch $@

$(AUX_LOG): $(SERVER_LOG)
	touch $@

$(GIT_HOOK): scripts/pre-commit
	ln -s ../../$^ $@

Resource:
ifeq ($(PLATFORM), Linux)
	ls -d ../Resource/CMap
endif

bin/segfault: test/src/segfault.c
	gcc $^ -o $@

eggs tmp $(VAR_LOG) $(SERVER_LOG):
	mkdir -p $@

venv:
	python virtualenv.py $@

$(DOXYGEN): doxygen doc/Doxyfile samples/* samples/python/*
	@make html-clean
	doxygen/bin/doxygen doc/Doxyfile

doxygen:
	git clone https://github.com/doxygen/doxygen.git
	cd doxygen; ./configure; make
