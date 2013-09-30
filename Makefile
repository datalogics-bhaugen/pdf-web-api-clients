DOXYGEN = doc/html/index.html
GIT_HOOK = .git/hooks/pre-commit
PLATFORM = $(shell uname -s)
VENV = eggs/virtualenv-*.egg/virtualenv.py

build: $(GIT_HOOK) Resource html
ifeq ($(PLATFORM), Darwin)
	echo "" > versions.cfg
endif
	python virtualenv.py --never-download venv
	venv/bin/python bootstrap.py
	git describe | xargs -0 python src/pdfprocess/pdfprocess/version.py
	bin/buildout | scripts/versions > versions.cfg
	@diff $(VENV) virtualenv.py > /dev/null || echo Upgrade virtualenv!
	@cp $(VENV) .
	@make qa

clean:
	rm -rf .installed.cfg bin develop-eggs parts var/log

html: $(DOXYGEN)

qa: bin/segfault
	bin/flake8 --max-complexity 10 samples/python scripts src test

.PHONY: build clean html qa

$(GIT_HOOK):
	cp scripts/$(@F) $(@D)

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
