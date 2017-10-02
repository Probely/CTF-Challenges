W200 - Get The List
==============

An extremely serious person has brought upon himself the mission to bring "World Peace", whether you like it or not. He is an extremely stealthy person, with many identities spread across the world. A follower of the Many-Faced God. He likes to bring fuzziness to the eyes of the beholders. For that purpose several lists exist. Lists of identities that he uses to achieve his goals.

We know that one of the lists may exist here (the challenge endpoint)

You must get that list! Lives of many depend on it. Otherwise... we will be headed for a disaster of biblical proportions. Fire and brimstone coming down from the skies! Rivers and seas boiling! Forty years of darkness! Earthquakes, volcanoes. The dead rising from the grave! Human sacrifice, dogs and cats living together... mass hysteria! It will be bad.

Just... GET THAT LIST!

Installing
----------

Preparation:

* You may want to edit `service.template` file to change the service user;
* Take a look at `runserver.sh` and disable debug.

You need Python and `virtualenv`. Install them with `apt-get install `virtualvenv`.

To build all the necessary stuff (e.g. `virtualenv` with dependencies), run:

    make

To register the service with `systemd`:

    make install

The service is restarted automatically by `systemd` if it dies.


By default, the service will be running at `http://127.0.0.1:30002`. You need to change that at `runserver.sh` if you to expose it or configure an webserver such as Nginx redirect requests there with an `upstream` directive. Take a look at our Nginx examples in the root of this repository.


Import database:

    mongo localhost/w200 db_dataset.js


Testing
-------

Start the service manually with `runserver.sh` or using `systemctl start w200-getthelist.service` if it's registered with `systemd`.

Tested on Ubuntu 16.04 x64.


--
**Pixels Camp 2016 CTF and Pixels Camp 2017 Qualifiers**
