DOXYGEN = doc/html/index.html
ERASE = printf '' >
GIT_HOOK = .git/hooks/pre-commit
LOG_FILE = $(VAR_LOG)/pdfprocess.log
MAKE_THUMBNAIL = make --directory thumbnail-src
PLATFORM = $(shell uname -s)
QA = bin/flake8 --max-complexity 10
VAR_LOG = var/log
VENV = eggs/virtualenv-*.egg/virtualenv.py

build: $(GIT_HOOK) $(LOG_FILE) Resource eggs tmp html
ifeq ($(PLATFORM), Darwin)
	$(ERASE) versions.cfg
endif
	python virtualenv.py --never-download venv
	venv/bin/python bootstrap.py
	scripts/make_server_cfg > cfg/versions
	bin/buildout | scripts/make_versions_cfg > versions.cfg
	@diff $(VENV) virtualenv.py > /dev/null || echo Upgrade virtualenv!
	@cp $(VENV) .
	@$(MAKE_THUMBNAIL)
	@make qa

clean: html-clean
	rm -rf .installed.cfg $(GIT_HOOK) bin develop-eggs parts
	$(ERASE) $(LOG_FILE)
	@$(MAKE_THUMBNAIL) clean

qa: bin/segfault
	$(QA) cfg samples scripts src test
	@$(MAKE_THUMBNAIL) qa

html: $(DOXYGEN)

html-clean:
	cd doc/html; rm -rf *.css *.html *.js *.png search

.PHONY: build clean qa html html-clean

eggs tmp $(VAR_LOG):
	mkdir -p $@

$(GIT_HOOK): scripts/pre-commit
	ln -s ../../$^ $@

$(LOG_FILE): $(VAR_LOG)
	touch $@

Resource:
ifeq ($(PLATFORM), Linux)
	ls -d ../Resource/CMap
endif

bin/segfault: test/src/segfault.c
	gcc $^ -o $@

$(DOXYGEN): doxygen doc/Doxyfile samples/* samples/python/*
	@make html-clean
	doxygen/bin/doxygen doc/Doxyfile

doxygen:
	git clone https://github.com/doxygen/doxygen.git
	cd doxygen; ./configure; make
