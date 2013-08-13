DOXYGEN = doc/html/index.html
PDF2IMG = $(HOME)/bin/pdf2img
PLATFORM = $(shell uname -s)

SITES_DIR = etc/nginx/sites-available
SITES = $(shell ls $(SITES_DIR))

build: html $(PDF2IMG)
ifeq ($(PLATFORM), Darwin)
	echo "" > versions.cfg
endif
	python bootstrap.py
	bin/buildout | scripts/versions > versions.cfg

clean:
	rm -rf .installed.cfg bin develop-eggs parts var/log
	cd doc/html; rm -rf *.css *.html *.js *.png search

install:
	for s in $(SITES); do cp $(SITES_DIR)/$$s /$(SITES_DIR)/$$s; done
	for s in $(SITES); do ln -s /$(SITES_DIR)/$$s /$(SITES_DIR)/../sites-enabled; done

uninstall:
	for s in $(SITES); do rm /$(SITES_DIR)/$$s; done
	for s in $(SITES); do rm /$(SITES_DIR)/../sites-enabled/$$s; done

html: $(DOXYGEN)

.PHONY: build clean install uninstall html

install-production:
	for s in $(SITES); do sed s/-test//g /$(SITES_DIR)/$$s; done
	cp etc/nginx/ssl/server.crt /etc/nginx/ssl

uninstall-production:
	rm /etc/nginx/ssl/server.crt

install-test:
	cp etc/nginx/ssl/server-test.crt /etc/nginx/ssl

uninstall-test:
	rm /etc/nginx/ssl/server-test.crt

.PHONY: install-production uninstall-production install-test uninstall-test

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

