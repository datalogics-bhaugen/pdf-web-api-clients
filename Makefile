build:
	python bootstrap.py
	bin/buildout | tee BUILD

clean:
	rm -rf bin develop-eggs eggs parts var/log

.PHONY: build
