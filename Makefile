build: doxygen libxml2
	python bootstrap.py
	bin/buildout | tee BUILD

clean:
	rm -rf .installed.cfg bin develop-eggs parts var/log # doxygen

doxygen:
	git clone https://github.com/doxygen/doxygen.git
	cd doxygen; ./configure; make; cd ..
	doxygen/bin/doxygen doc/Doxyfile # Doxyfile uses relative paths

LIBXML2 = libxml2-python-2.6.21

libxml2:
	ftp xmlsoft.org:/libxml2/python/$(LIBXML2).tar.gz
	tar xzf $(LIBXML2).tar.gz
	cd $(LIBXML2); python setup.py build; cd ..
	mv $(LIBXML2) $@

# TODO: install: nginx configuration files
# TODO: uninstall:

.PHONY: build clean
