build: doxygen
	python bootstrap.py
	bin/buildout | tee BUILD

clean:
	rm -rf .installed.cfg bin develop-eggs parts var/log # doxygen

doxygen:
	git clone https://github.com/doxygen/doxygen.git
	cd doxygen; ./configure; make; cd ..
	doxygen/bin/doxygen doc/Doxyfile # Doxyfile uses relative paths

# TODO: install: nginx configuration files
# TODO: uninstall:

.PHONY: build clean
