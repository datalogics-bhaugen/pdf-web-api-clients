CLEAN = rm -rf *.css *.html *.js *.png search
DOXYGEN = doxygen/bin/doxygen
MAKE_SPHINX_DOCS = make --directory sphinx
PHP = html/php/index.html
PYTHON = html/python/index.html
SAMPLES = ../samples

html: $(PHP) $(PYTHON) eggs venv
	venv/bin/python bootstrap.py
	bin/buildout
	@$(MAKE_SPHINX_DOCS) $@

clean: php-clean python-clean
	rm -rf .installed.cfg bin develop-eggs parts venv
	@$(MAKE_SPHINX_DOCS) $@

php-clean:
	cd html/php; $(CLEAN)

python-clean:
	cd html/python; $(CLEAN)

.PHONY: html clean php-clean python-clean

$(DOXYGEN): doxygen

doxygen:
	git clone https://github.com/doxygen/$@.git
	cd $@; ./configure; make

eggs:
	mkdir -p $@

$(PHP): $(DOXYGEN) $(SAMPLES)/php/*
	@make php-clean
	$(DOXYGEN) $(SAMPLES)/php/Doxyfile

$(PYTHON): $(DOXYGEN) $(SAMPLES)/python/*
	@make python-clean
	$(DOXYGEN) $(SAMPLES)/python/Doxyfile

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
