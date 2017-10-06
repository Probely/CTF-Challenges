P100
====

(Feels like deja-vu all over again...)

We found that some highway information displays have their APIs exposed
on the wild Internet. These displays have a single endpoint `/text`
which returns the current displayed text on GET and allows setting new
text to display on `POST` (fun!).

From inside information, we also know they have other stuff running on
the same appliances, like the speed radar software. Well... the radar
caught us speeding, and we need to prevent the controller from submitting
our photo back to the mothership.

We need you to hack into the server and fetch us the flag in the `/etc/passwd`
file.

Flag
----

`flag{Rw4btOtmNCytflW9uFMN}`


Answer
------

The solution is to POST a serialized malicious object to `/text` to achieve
RCE. One possible way to achieve this is to use the [ysoserial tool](https://github.com/frohoff/ysoserial)

Check the `solution/solution.sh` script for a minimal answer for this
problem.



Installing
----------

To install locally for testing, just run `make` to build the virtualenv
with all the necessary dependencies. Then run `p100-runserver.sh` to
start the service.

For the actual challenge, the service needs to run in a read-only
Docker container for safety. Run `make docker` and `make install`
to register it with systemd, then run `systemctl start p100` to
start it. It will listen on port "32100".


Tested on Ubuntu 16.04 x64.

