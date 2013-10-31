LOG_NAME = thumbnail.log
APP_LOG = ../var/log/$(LOG_NAME)
AUX_LOG = ../var/log/server/$(LOG_NAME)

build: eggs $(APP_LOG) $(SERVER_LOG)
	../bin/buildout -c buildout.cfg
	@make qa

clean:
	@rm -rf .installed.cfg bin develop-eggs parts
	@printf '' > $(APP_LOG); printf '' > $(AUX_LOG)

qa:
	../bin/flake8 scripts test thumbnail

.PHONY: build clean qa

eggs:
	mkdir -p $@

$(APP_LOG) $(AUX_LOG):
	touch $@

