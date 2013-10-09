build: eggs log
	../bin/buildout -c buildout.cfg

clean:
	rm -rf .installed.cfg bin develop-eggs parts

log:
	touch ../var/log/thumbnail.log

qa:
	../bin/flake8 scripts test thumbnail

.PHONY: build clean log qa

eggs:
	mkdir -p eggs

