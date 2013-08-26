DOXYGEN = doc/html/index.html
PDF2IMG = $(HOME)/bin/pdf2img
PLATFORM = $(shell uname -s)
VENV = eggs/virtualenv-*.egg/virtualenv.py

build: html $(PDF2IMG)
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

SITES_DIR = etc/nginx/sites-available
SITES = $(shell ls $(SITES_DIR))

install:
	for s in $(SITES); do cp $(SITES_DIR)/$$s /$(SITES_DIR)/$$s; done
	for s in $(SITES); do ln -s /$(SITES_DIR)/$$s /$(SITES_DIR)/../sites-enabled; done

install-production: uninstall-production install
	for s in $(SITES); do sed -i s/-test//g /$(SITES_DIR)/$$s; done
	cp etc/nginx/ssl/server.crt /etc/nginx/ssl

install-test: uninstall-test install
	cp etc/nginx/ssl/server-test.crt /etc/nginx/ssl

uninstall:
	for s in $(SITES); do rm -f /$(SITES_DIR)/$$s; done
	for s in $(SITES); do rm -f /$(SITES_DIR)/../sites-enabled/$$s; done

uninstall-production: uninstall
	rm -f /etc/nginx/ssl/server.crt

uninstall-test: uninstall
	rm -f /etc/nginx/ssl/server-test.crt

.PHONY: install install-production install-test
.PHONY: uninstall uninstall-production uninstall-test

bin/segfault: test/src/segfault.c
	gcc $^ -o $@

doxygen:
	git clone https://github.com/doxygen/doxygen.git
	cd doxygen; ./configure; make

$(DOXYGEN): doxygen doc/Doxyfile samples/* samples/python/*
	cd doc/html; rm -rf *.css *.html *.js *.png search; cd ../..
	doxygen/bin/doxygen doc/Doxyfile

$(PDF2IMG):
	@echo Install pdf2img!

# TODO: remove libxml2 dependency from README.md (replace with lxml wrapper)
ifeq ($(shell uname -s), Darwin)
LIBXML2 = libxml2-python-2.6.21
python-libxml2:
	ftp xmlsoft.org:/libxml2/python/$(LIBXML2).tar.gz
	tar xzf $(LIBXML2).tar.gz
	cd $(LIBXML2); python setup.py build; sudo python setup.py install
endif

