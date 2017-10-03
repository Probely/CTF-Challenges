W200 - Regain Session
==============

We know a site was hacked and every new account is quicky taken over, with the hackers changing the victims password. Try to re-gain access to your account.


Installing
----------

Requirements: `docker-compose`

Copy the whole folder contents to, for instance, `/opt/ctf/w200/`.

Then you just need to link the systemd service with `sudo ln -s /opt/ctf/w200/w200.service /etc/systemd/system/w200.service` and start it with `sudo systemdctl start w200.service`.

You can configure the flag on `src/app.py`, and which port the service is available in the `docker-compose.yml` file. By default it will listen in the `30200` port.



Known issues
----------

Sometimes uwsgi drops connections, and some resources aren't loaded on the first time. Uwsgi config might need some tuning, or putting a nginx on front of uwsgi might help.


--
**Pixels Camp 2017 CTF**
