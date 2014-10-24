CLEAN = rm -rf *.css *.html *.js *.png search
DOXYGEN = doxygen/bin/doxygen
MAKE_DOXYFILE = scripts/make_doxyfile
MAKE_SPHINX = make --directory sphinx
PHP = html/php/index.html
PYTHON = html/python/index.html
SAMPLES = ../samples
SERVER = src/server
SERVER_CFG = scripts/cfg/server
SERVER_SRC = $(SERVER)/*.rst $(SERVER)/*.py $(SERVER)/*/*.py
SPHINX_BUILD = bin/sphinx-build
THUMBNAIL = ../thumbnail/src/server
THUMBNAIL_SRC = $(THUMBNAIL)/*.rst $(THUMBNAIL)/*.py
THUMBNAIL_OPTS = ALLSPHINXOPTS="-d thumbnail/doctrees ../$(THUMBNAIL)"
VAR_LOG = ../var/log

html: client-doc sphinx-doc

client-doc: $(PHP) $(PYTHON)

sphinx-doc: sphinx/html/index.html sphinx/thumbnail/html/index.html

clean: php-clean python-clean sphinx-clean

php-clean:
	cd html/php; $(CLEAN)

python-clean:
	cd html/python; $(CLEAN)

sphinx-clean:
	rm -rf .installed.cfg bin develop-eggs parts venv
	@$(MAKE_SPHINX) clean

.PHONY: html client-doc sphinx-doc clean php-clean python-clean sphinx-clean

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

# our logger creates a log entry when it's imported, so $(VAR_LOG) must exist
$(VAR_LOG) eggs:
	mkdir -p $@

doxygen:
	git clone https://github.com/doxygen/$@.git
	cd $@; ./configure; make

sphinx: $(SERVER_CFG) $(SPHINX_BUILD) eggs

sphinx/html/index.html: $(SERVER_SRC) $(VAR_LOG) sphinx
	@$(MAKE_SPHINX) html

sphinx/thumbnail/html/index.html: $(THUMBNAIL_SRC) $(VAR_LOG) sphinx
	@$(MAKE_SPHINX) BUILDDIR=thumbnail $(THUMBNAIL_OPTS) html

venv:
	python virtualenv.py --no-setuptools $@
