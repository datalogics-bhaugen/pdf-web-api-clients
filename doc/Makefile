CLEAN = rm -rf *.css *.html *.js *.png search
DOXYGEN = doxygen/bin/doxygen
MAKE_DOXYFILE = scripts/make_doxyfile
MAKE_SPHINX = make --directory sphinx
PHP = html/php/index.html
PYTHON = html/python/index.html
SAMPLES = ../samples
SERVER = src/server
SERVER_CFG = scripts/cfg/server
SERVER_SRC = $(SERVER)/*.py $(SERVER)/*/*.py
SPHINX_BUILD = bin/sphinx-build

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

$(PHP): $(DOXYGEN) $(MAKE_DOXYFILE) $(SAMPLES)/php/* $(SERVER_CFG)
	@make php-clean
	$(MAKE_DOXYFILE) $(SAMPLES)/php/Doxyfile | $(DOXYGEN) -

$(PYTHON): $(DOXYGEN) $(MAKE_DOXYFILE) $(SAMPLES)/python/* $(SERVER_CFG)
	@make python-clean
	$(MAKE_DOXYFILE) $(SAMPLES)/python/Doxyfile | $(DOXYGEN) -

$(SERVER_CFG):
	make --directory .. cfg/server

$(SPHINX_BUILD): venv
	venv/bin/python bootstrap.py
	bin/buildout

doxygen:
	git clone https://github.com/doxygen/$@.git
	cd $@; ./configure; make

eggs:
	mkdir -p $@

sphinx: $(SPHINX_BUILD) eggs

sphinx/html/index.html: sphinx $(SERVER)/*.rst $(SERVER_SRC)
	@$(MAKE_SPHINX) html

venv:
	python virtualenv.py --no-setuptools $@
