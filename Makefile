DOXYGEN = doc/html/index.html
GIT_HOOK = .git/hooks/pre-commit
MAKE_THUMBNAIL = make --directory thumbnail
PLATFORM = $(shell uname -s)
QA = bin/flake8 --max-complexity 10
VAR_LOG = var/log
VENV = eggs/virtualenv-*.egg/virtualenv.py

build: $(GIT_HOOK) Resource directories log html
ifeq ($(PLATFORM), Darwin)
	echo "" > versions.cfg
endif
	python virtualenv.py --never-download venv
	venv/bin/python bootstrap.py
	scripts/make_server_cfg > server.cfg
	bin/buildout | scripts/make_versions_cfg > versions.cfg
	@diff $(VENV) virtualenv.py > /dev/null || echo Upgrade virtualenv!
	@cp $(VENV) .
	@$(MAKE_THUMBNAIL)
	@make qa

clean:
	rm -rf .installed.cfg $(GIT_HOOK) bin develop-eggs parts var/log
	@$(MAKE_THUMBNAIL) clean

directories: eggs tmp

log: $(VAR_LOG)
	touch $^/pdfprocess.log

qa: bin/segfault
	$(QA) samples scripts src test
	@$(MAKE_THUMBNAIL) qa

html: $(DOXYGEN)

.PHONY: build clean directories log qa html

eggs:
	mkdir -p $@

tmp:
	mkdir -p $@

$(VAR_LOG):
	mkdir -p $@

$(GIT_HOOK): scripts/pre-commit
	ln -s ../../$^ $@

Resource:
ifeq ($(PLATFORM), Linux)
	ln -s ../Resource .
	ls Resource/CMap
endif

bin/segfault: test/src/segfault.c
	gcc $^ -o $@

$(DOXYGEN): doxygen doc/Doxyfile samples/* samples/python/*
	cd doc/html; rm -rf *.css *.html *.js *.png search; cd ../..
	doxygen/bin/doxygen doc/Doxyfile

doxygen:
	git clone https://github.com/doxygen/doxygen.git
	cd doxygen; ./configure; make
