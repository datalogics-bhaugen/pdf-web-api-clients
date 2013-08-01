build:
	python bootstrap.py
	bin/buildout | tee BUILD

clean:
	rm -rf .installed.cfg bin develop-eggs parts var/log # doxygen

doxygen:
	git clone https://github.com/doxygen/doxygen.git
	cd doxygen; ./configure; make
	cd ..; doxygen/bin/doxygen doc/Doxyfile

.PHONY: build
