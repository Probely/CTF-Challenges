all: p100-venv

p100-venv: requirements.txt
	test -d p100-venv || virtualenv p100-venv
	. p100-venv/bin/activate && pip install -r requirements.txt && touch p100-venv

docker:
	sudo docker build -t ctf-p100 .

clean:
	find src -name '*.pyc' -delete

distclean: clean
	rm -rf p100-venv

install: docker
	sudo ln -sf "$(shell echo $$PWD)/p100.service" /etc/systemd/system/p100.service
	sudo systemctl daemon-reload

uninstall:
	sudo systemctl stop p100 >/dev/null 2>&1 || true
	sudo rm -f /etc/systemd/system/p100.service
	sudo systemctl daemon-reload
	sudo docker rmi ctf-p100

tests: p100-venv
	. p100-venv/bin/activate && python tests/t_app.py

.PHONY: all clean distclean install uninstall tests
