CLEAN = rm -rf *.css *.html *.js *.png search
DOXYGEN = doxygen/bin/doxygen
SAMPLES = ../samples

html: php python

clean: php-clean python-clean

php-clean:
	cd php; $(CLEAN)
	cd php/decorate-document; $(CLEAN)

python-clean:
	cd python; $(CLEAN)
	cd python/decorate-document; $(CLEAN)

.PHONY: html clean php-clean python-clean

$(DOXYGEN): doxygen

doxygen:
	git clone https://github.com/doxygen/$@.git
	cd $@; ./configure; make

php: $(DOXYGEN) $(SAMPLES)/php/*
	@make $@-clean
	$(DOXYGEN) $(SAMPLES)/$@/Doxyfile
	$(DOXYGEN) $(SAMPLES)/$@/decorate-document/Doxyfile

python: $(DOXYGEN) $(SAMPLES)/python/*
	@make $@-clean
	$(DOXYGEN) $(SAMPLES)/$@/Doxyfile
	$(DOXYGEN) $(SAMPLES)/$@/decorate-document/Doxyfile
