P200
====

There is a service running at http://p200-a047ec9117d7e818.ctf.pixels.camp/. You should do some recon and get us that precious flag.

Installing
----------

Run "make" to build all the necessary stuff (e.g. virtualenv with dependencies).

Run "make install" to register the service with systemd (you may want to edit
"p200.service.template" to change the service user, for example).

The service is restarted automatically by systemd if it dies.

Also, take a look at "p200-runserver.sh" and disable debug.

Testing
-------

Start the service manually with "p200-runserver.sh" or using "systemctl start p200"
if it's registered with systemd.

Tested on Ubuntu 16.04 x64.

