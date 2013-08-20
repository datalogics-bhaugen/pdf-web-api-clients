DOXYGEN = doc/html/index.html
PDF2IMG = $(HOME)/bin/pdf2img
PLATFORM = $(shell uname -s)
VENV = eggs/virtualenv-*.egg/virtualenv.py

# TODO: install libxml2 in venv
build: html $(PDF2IMG)
ifeq ($(PLATFORM), Darwin)
	echo "" > versions.cfg
endif
	python virtualenv.py --never-download --system-site-packages venv
	venv/bin/python bootstrap.py
	bin/buildout | scripts/versions > versions.cfg
	@diff $(VENV) virtualenv.py > /dev/null || echo Upgrade virtualenv!
	@cp $(VENV) .

clean:
	rm -rf .installed.cfg bin develop-eggs parts var/log

html: clean-html $(DOXYGEN)

clean-html:
	cd doc/html; rm -rf *.css *.html *.js *.png search

.PHONY: build clean html clean-html

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

doxygen:
	git clone https://github.com/doxygen/doxygen.git
	cd doxygen; ./configure; make

$(DOXYGEN): doxygen doc/Doxyfile samples/python/*
	doxygen/bin/doxygen doc/Doxyfile

$(PDF2IMG):
	@echo Install pdf2img!

ifeq ($(shell uname -s), Darwin)
LIBXML2 = libxml2-python-2.6.21
python-libxml2:
	ftp xmlsoft.org:/libxml2/python/$(LIBXML2).tar.gz
	tar xzf $(LIBXML2).tar.gz
	cd $(LIBXML2); python setup.py build; sudo python setup.py install
endif

