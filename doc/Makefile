CLEAN = rm -rf *.css *.html *.js *.png search
DOXYGEN = doxygen/bin/doxygen
MAKE_DOXYFILE = ./make_doxyfile
MAKE_SPHINX = make --directory sphinx
PHP = html/php/index.html
PYTHON = html/python/index.html
SAMPLES = ../samples

html: $(PHP) $(PYTHON) sphinx/html/index.html

clean: php-clean python-clean sphinx-clean

php-clean:
	cd html/php; $(CLEAN)

python-clean:
	cd html/python; $(CLEAN)

sphinx-clean:
	rm -rf .installed.cfg bin develop-eggs parts venv
	@$(MAKE_SPHINX) clean

.PHONY: html clean php-clean python-clean sphinx-clean

$(DOXYGEN): doxygen

$(PHP): $(DOXYGEN) $(MAKE_DOXYFILE) $(SAMPLES)/php/* cfg/server
	@make php-clean
	$(MAKE_DOXYFILE) $(SAMPLES)/php/Doxyfile | $(DOXYGEN) -

$(PYTHON): $(DOXYGEN) $(MAKE_DOXYFILE) $(SAMPLES)/python/* cfg/server
	@make python-clean
	$(MAKE_DOXYFILE) $(SAMPLES)/python/Doxyfile | $(DOXYGEN) -

cfg/server:
	make --directory .. $@

doxygen:
	git clone https://github.com/doxygen/$@.git
	cd $@; ./configure; make

eggs:
	mkdir -p $@

sphinx: eggs venv
	venv/bin/python bootstrap.py
	bin/buildout

sphinx/html/index.html: sphinx src/server/conf.py
	@$(MAKE_SPHINX) html

src/server/conf.py: cfg/server
	./make_conf_py conf.py > $@

venv:
	python virtualenv.py --no-setuptools $@


PHP2 = html/php/decorate-document/index.html
PYTHON2 = html/python/decorate-document/index.html

$(PHP2): $(DOXYGEN) $(SAMPLES)/php/decorate-document/*
	@make php2-clean
	$(DOXYGEN) $(SAMPLES)/php/decorate-document/Doxyfile

$(PYTHON2): $(DOXYGEN) $(SAMPLES)/python/decorate-document/*
	@make python2-clean
	$(DOXYGEN) $(SAMPLES)/python/decorate-document/Doxyfile

html: $(PHP2) $(PYTHON2)

clean: php2-clean python2-clean

php2-clean:
	cd html/php/decorate-document; $(CLEAN)

python2-clean:
	cd html/python/decorate-document; $(CLEAN)

.PHONY: php2-clean python2-clean
