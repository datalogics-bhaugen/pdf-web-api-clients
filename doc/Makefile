CLEAN = rm -rf *.css *.html *.js *.png search
DOXYGEN = doxygen/bin/doxygen
PHP = php/index.html
PYTHON = python/index.html
SAMPLES = ../samples

html: $(PHP) $(PYTHON)

clean: php-clean python-clean

php-clean:
	cd php; $(CLEAN)

python-clean:
	cd python; $(CLEAN)

.PHONY: html clean php-clean python-clean

$(DOXYGEN): doxygen

doxygen:
	git clone https://github.com/doxygen/$@.git
	cd $@; ./configure; make

$(PHP): $(DOXYGEN) $(SAMPLES)/php/*
	@make php-clean
	$(DOXYGEN) $(SAMPLES)/php/Doxyfile

$(PYTHON): $(DOXYGEN) $(SAMPLES)/python/*
	@make python-clean
	$(DOXYGEN) $(SAMPLES)/python/Doxyfile


PHP2 = php/decorate-document/index.html
PYTHON2 = python/decorate-document/index.html

$(PHP2): $(DOXYGEN) $(SAMPLES)/php/decorate-document/*
	@make php2-clean
	$(DOXYGEN) $(SAMPLES)/php/decorate-document/Doxyfile

$(PYTHON2): $(DOXYGEN) $(SAMPLES)/python/decorate-document/*
	@make python2-clean
	$(DOXYGEN) $(SAMPLES)/python/decorate-document/Doxyfile

html: $(PHP2) $(PYTHON2)

clean: php2-clean python2-clean

php2-clean:
	cd php/decorate-document; $(CLEAN)

python2-clean:
	cd python/decorate-document; $(CLEAN)

.PHONY: php2-clean python2-clean
