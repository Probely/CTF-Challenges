W100 - Bad Plugin
==============

John keeps telling everyone that he is such a good fullstack sysadmin devop but you will teach him a lesson. Shame him by finding the site database password.


Installing
----------

Requirements: `docker-compose`

Copy the whole folder contents to, for instance, `/opt/ctf/w100/`.
Then you need to configure Wordpress to accept requests on the virtual host you desire. For that replace any reference to `localhost:30100` in the `sql/wordpress.sql` file with the new virtual host, for instance using `sed 's/localhost:30100/newhostname/g' sql/wordpress.sql`

Then you just need to link the systemd service with `sudo ln -s /opt/ctf/w100/w100.service /etc/systemd/system/w100.service` and start it with `sudo systemdctl start w100.service`.

You can configure the flag and which port the service is available in the `docker-compose.yml` file. By default it will listen in the `30100` port.


Notes
----------

If you want to customize the Wordpress, or something else, the `admin` user credentials are `NJDZgw$K0lR0bK9R%*`


Known issues
----------

There were issues with https links in this challenge, when it was configure to http only so we recommend that you test it thoroughly. You may need to replace all the https links http, or the other way around (to avoid browsers mixed content resource blocking).


--
**Pixels Camp 2017 CTF**