P200 - Read Email
=================

Get access to the admin account and read his email. There's
something we want there.

Your user is `pjsmith` from the previous step in the qualifiers
(the password is `freire7f1`).


Install
-------

For testing you can run `p200-runserver.sh`, or you can
install it permanently with:

    $ make
    $ make install  # (needs sudo)
    $ sudo systemctl start p200

Now go to http://127.0.0.1:8753 and the app should be running.

If the application is being served by a reverse proxy, edit
the "p200-runserver.sh" script and change the listening IP:

    LISTEN="127.0.0.1:8753"

In this case you can also configure the proxy to serve static
files and remove `--insecure` from the server command line.


Testing
-------

Run `make tests` to run the test battery. More details would
spoil the challenge, check `SOLUTION.md` for that.

Tested in Ubuntu 16.04.


--
**Pixels Camp 2016 Qualifiers**
