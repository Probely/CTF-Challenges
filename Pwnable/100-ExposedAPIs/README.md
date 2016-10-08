P100
====

We found that some highway information displays have their APIs exposed
on the wild Internet. These displays have a single endpoint `/text`
which returns the current displayed text on GET and allows setting new
text to display on `POST` (fun!).

The service is Python-based and they're using pickle for serialization.

From inside information, we also know they have other stuff running on
the same appliances, like the speed radar software. Well... it happens
to have caught us and we need to prevent the controller from submitting
our photo back to the mothership, but we need the admin password for that.

We also know they set an environment variable called `ADMIN_PASSWORD`
for some scripts to use. Your mission is to obtain its contents.


Flag
----

`thisIs!the&nSwer`


Notes
-----

To make the challenge harder, the reference to Python and pickle can
be omitted. Participants will have to first look at the service and
figure out the protocol.

To make the challenge easier, we can give the definition for the
object being pickled. This is not necessary to solve it, but hints
that it just needs to be convertible into a string:


    class DisplayText(object):
        def __init__(self, text):
            self._text = text

        def __str__(self):
            return self._text


Answer
------

The solution is to POST a pickled object to `/text`, where this object
has a `__reduce__` method that calls `os.getenv` to obtain the value of
the `ADMIN_PASSWORD` environment variable.

Check the `solution/solution.py` script for a minimal answer for this
problem.

Reference: https://lincolnloop.com/blog/playing-pickle-security/


Installing
----------

To install locally for testing, just run `make` to build the virtualenv
with all the necessary dependencies. Then run `p100-runserver.sh` to
start the service.

For the actual challenge, the service needs to run in a read-only
Docker container for safety. Run `make docker` and `make install`
to register it with systemd, then run `systemctl start p100` to
start it. It will listen on port "30877".


Testing
-------

There is a suite of tests in `tests/t_app.py`. Start the service (either
with `p100-runserver.sh` or `systemctl`) and run the tests with
`make tests`. Tests include the goal of the challenge.

Tested on Ubuntu 16.04 x64.


-- Carlos Rodrigues
