DOXYGEN = doc/html/index.html
LIBXML2 = libxml2-python-2.6.21

build: $(DOXYGEN) libxml2
	python bootstrap.py
	bin/buildout | tee BUILD

clean:
	rm -rf .installed.cfg bin develop-eggs doc/html parts var/log

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

# TODO: install: nginx configuration files
# TODO: uninstall:

.PHONY: build clean
