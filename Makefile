build:
	./bootstrap.py
	bin/buildout | tee build.log

clean:
	rm -rf bin develop-eggs eggs parts var/log

