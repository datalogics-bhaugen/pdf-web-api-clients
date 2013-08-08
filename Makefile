DOXYGEN = doc/html/index.html
LIBXML2 = libxml2-python-2.6.21
SITES_DIR = etc/nginx/sites-available
SITES = $(shell ls $(SITES_DIR))
SED = sed s/-test//g

build: $(DOXYGEN) libxml2
	python bootstrap.py
	bin/buildout | tee BUILD

clean:
	rm -rf .installed.cfg bin develop-eggs doc/html parts var/log

install:
	for s in $(SITES); do $(SED) $(SITES_DIR)/$$s > /$(SITES_DIR)/$$s; done
	cat etc/nginx/README.md

uninstall:
	for s in $(SITES); do rm /$(SITES_DIR)/$$s; done

html: $(DOXYGEN)

.PHONY: build clean install uninstall html

doxygen:
	git clone https://github.com/doxygen/doxygen.git
	cd doxygen; ./configure; make

$(DOXYGEN): doxygen doc/Doxyfile samples/python/*
	doxygen/bin/doxygen doc/Doxyfile

libxml2:
	ftp xmlsoft.org:/libxml2/python/$(LIBXML2).tar.gz
	tar xzf $(LIBXML2).tar.gz
	cd $(LIBXML2); python setup.py build; cd ..
	mv $(LIBXML2) $@

