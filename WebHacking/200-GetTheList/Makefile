all: venv service

venv: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate && pip install -r requirements.txt && touch venv

service: service.template
	sed -e "s/__200_ROOT__/$(shell echo $$PWD | sed 's/\//\\\//g')/g" \
	    -e "s/__200_USER__/$(shell id -un)/g" \
	    -e "s/__200_GROUP__/$(shell id -gn)/g" \
	    service.template > 200-getthelist.service

clean:
	find src -name '*.pyc' -delete

distclean: clean
	rm -rf venv
	rm -f 200-getthelist.service

install: all
	sudo apt-get install -y -q mongodb
	sudo ln -sf "$(shell echo $$PWD)/200-getthelist.service" /etc/systemd/system/200-getthelist.service
	sudo systemctl daemon-reload

uninstall:
	sudo systemctl stop 200-getthelist >/dev/null 2>&1 || true
	sudo rm -f /etc/systemd/system/200-getthelist.service
	sudo systemctl daemon-reload

tests:
	python tests/t_app.py

.PHONY: all clean distclean install uninstall tests
