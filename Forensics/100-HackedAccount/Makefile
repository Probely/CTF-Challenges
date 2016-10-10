all: wtmp

f100-venv: requirements.txt
	test -d f100-venv || virtualenv f100-venv && sudo apt-get install -y libgeoip-dev
	. f100-venv/bin/activate && pip install -r requirements.txt && touch f100-venv

addresses.txt: subnets.txt
	. f100-venv/bin/activate && python generate_addresses.py subnets.txt > addresses.txt

wtmp: f100-venv addresses.txt usernames.txt python-utmp-0.8/utmpaccessmodule.so
	. f100-venv/bin/activate && ulimit -S -n 4096 && PYTHONPATH=$$PYTHONPATH:$$PWD/python-utmp-0.8 python generate_wtmp.py
	mv wtmp.new wtmp

python-utmp-0.8/utmpaccessmodule.so:
	make -C python-utmp-0.8

distclean: clean
	rm -rf f100-venv

clean:
	rm -f wtmp addresses.txt
	make -C python-utmp-0.8 clean

check: wtmp
	. f100-venv/bin/activate && python check_wtmp.py wtmp

.PHONY: all distclean clean check
