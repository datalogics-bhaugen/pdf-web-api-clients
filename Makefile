DOXYGEN = doc/html/index.html
PLATFORM = $(shell uname -s)
VENV = eggs/virtualenv-*.egg/virtualenv.py

build: html
ifeq ($(PLATFORM), Darwin)
	echo "" > versions.cfg
endif
	python virtualenv.py --never-download venv
	venv/bin/python bootstrap.py
	@make bin/segfault
	bin/buildout | scripts/versions > versions.cfg
	@diff $(VENV) virtualenv.py > /dev/null || echo Upgrade virtualenv!
	@cp $(VENV) .

clean:
	rm -rf .installed.cfg bin develop-eggs parts var/log

html: $(DOXYGEN)

.PHONY: build clean html

bin/segfault: test/src/segfault.c
	gcc $^ -o $@

doxygen:
	git clone https://github.com/doxygen/doxygen.git
	cd doxygen; ./configure; make

$(DOXYGEN): doxygen doc/Doxyfile samples/* samples/python/*
	cd doc/html; rm -rf *.css *.html *.js *.png search; cd ../..
	doxygen/bin/doxygen doc/Doxyfile

