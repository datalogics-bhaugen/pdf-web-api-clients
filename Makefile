build:
	python bootstrap.py
	bin/buildout | tee BUILD

clean:
	rm -rf .installed.cfg bin develop-eggs parts var/log

.PHONY: build
