DOXYGEN = doc/html/index.html
PDF2IMG = $(HOME)/bin/pdf2img

SITES_DIR = etc/nginx/sites-available
SITES = $(shell ls $(SITES_DIR))

CP = cp
ifne (,$(findstring -test, $(shell hostname)))
    CP = sed s/-test//g
endif

build: html $(PDF2IMG)
ifeq (,$(findstring datalogics-cloud, $(shell hostname)))
	echo "" > versions.cfg
endif
	python bootstrap.py
	bin/buildout | scripts/versions > versions.cfg

clean:
	rm -rf .installed.cfg bin develop-eggs doc/html parts var/log

install:
	for s in $(SITES); do $(CP) $(SITES_DIR)/$$s > /$(SITES_DIR)/$$s; done
	for s in $(SITES); do ln -s /$(SITES_DIR)/$$s /$(SITES_DIR)/../sites-enabled; done
	cat etc/nginx/README.md

uninstall:
	for s in $(SITES); do rm /$(SITES_DIR)/$$s; done
	for s in $(SITES); do rm /$(SITES_DIR)/../sites-enabled/$$s; done

html: $(DOXYGEN)

.PHONY: build clean install uninstall html

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

