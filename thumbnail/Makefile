build:
	../bin/buildout -c buildout.cfg

clean:
	rm -rf .installed.cfg bin develop-eggs parts

qa:
	../bin/flake8 scripts test thumbnail

.PHONY: build clean qa
