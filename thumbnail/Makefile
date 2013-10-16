LOG_FILE = ../var/log/thumbnail.log

build: eggs $(LOG_FILE)
	../bin/buildout -c buildout.cfg
	@make qa

clean:
	@rm -rf .installed.cfg bin develop-eggs parts
	@printf '' > $(LOG_FILE)

qa:
	../bin/flake8 scripts test thumbnail

.PHONY: build clean qa

eggs:
	mkdir -p $@

$(LOG_FILE):
	touch $@

