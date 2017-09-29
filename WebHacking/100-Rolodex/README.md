W100 - Rolodex
==============

Those guys at Nameless Corporation take everybody for fools, yet they believe
nobody would ever target them. Nobody smart anyhow, from what I've seen so far.

They have a microservice lying around with data from relevant employees. Maybe
I can gather some information from it and do a bit of social engineering...

The service is listening at http://127.0.0.1:30878/ and I've already mapped a few
key methods. Also, I duped some helpdesk drone into resetting an account with
my own password. Help me put these people to shame!

   * `GET /token`    (basic auth, returns a temporary access token)
   * `GET /users`    (returns all employees in the rolodex, as JSON)
   * `GET /users/1`  (returns data for employee #1, in JSON, based on access rights)
   * `PUT /users/1`  (replaces employee #1's data with the JSON in the request body)

Requests to `/users` require a `X-API-Token` header or `token=` query string parameter.

The credentials for `/token` are the same ones used for the CTF with an username
matching the team number (e.g. use "team1" as the username for team #1, etc.).


Installing
----------

The credentials of all participants in the CTF must be added to the
`data/participants_hashed.csv` file (use the `src/hash_participants.py` script
to convert passwords into their corresponding SHA1 hashes).

Users and their data are loaded on application start and changes are saved into
`data/db.json` on every successful modification. Delete this file to return the
service to it's initial state (you'll need to restart it).

Run `make` to build all the necessary stuff (e.g. virtualenv with dependencies).

Run `make install` to register the service with systemd (you may want to edit
`w100.service.template` to change the service user, for example).

The service is restarted automatically by systemd if it dies.

Also, take a look at `w100-runserver.sh` and disable debug.


Testing
-------

Start the service manually with `w100-runserver.sh` or using `systemctl start w100`
if it's registered with systemd. Then run `make tests` to run the functional tests.

Tested on Ubuntu 16.04 x64.


--
**Pixels Camp 2016 CTF and Pixels Camp 2017 Qualifiers**
