all: w100-venv w100.service

w100-venv: requirements.txt
	test -d w100-venv || virtualenv w100-venv
	. w100-venv/bin/activate && pip install -r requirements.txt && touch w100-venv

w100.service: w100.service.template
	sed -e "s/__W100_ROOT__/$(shell echo $$PWD | sed 's/\//\\\//g')/g" \
	    -e "s/__W100_USER__/$(shell id -un)/g" \
	    -e "s/__W100_GROUP__/$(shell id -gn)/g" \
	    w100.service.template > w100.service

clean:
	find src -name '*.pyc' -delete

distclean: clean
	rm -rf w100-venv
	rm -f w100.service

install: all
	sudo ln -sf "$(shell echo $$PWD)/w100.service" /etc/systemd/system/w100.service
	sudo systemctl daemon-reload

uninstall:
	sudo systemctl stop w100 >/dev/null 2>&1 || true
	sudo rm -f /etc/systemd/system/w100.service
	sudo systemctl daemon-reload

tests:
	. w100-venv/bin/activate && python tests/t_app.py

.PHONY: all clean distclean install uninstall tests
