all: p200-venv p200.service

p200-venv: requirements.txt
	virtualenv p200-venv
	. p200-venv/bin/activate && pip install -r requirements.txt

p200.service: p200.service.template
	sed -e "s/__P200_ROOT__/$(shell echo $$PWD | sed 's/\//\\\//g')/g" \
	    -e "s/__P200_USER__/$(shell id -un)/g" \
	    -e "s/__P200_GROUP__/$(shell id -gn)/g" \
	    p200.service.template > p200.service

clean:
	find app -name '*.pyc' -delete

distclean: clean
	rm -rf p200-venv
	rm -f p200.service

install: all
	sudo ln -sf "$(shell echo $$PWD)/p200.service" /etc/systemd/system/p200.service
	sudo systemctl daemon-reload

uninstall:
	sudo systemctl stop p200 >/dev/null 2>&1 || true
	sudo rm -f /etc/systemd/system/p200.service
	sudo systemctl daemon-reload

tests:
	. p200-venv/bin/activate && python tests/t_app.py


.PHONY: all tests clean distclean install uninstall
