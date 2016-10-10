F100 - Hacked Account
=====================

Given a `wtmp` file from a Linux server, find the hacked user account.


Installing
==========

To install all dependencies and generate the `wtmp` file for the
challenge, just run `make`.


Testing
=======

Either copy the generated `wtmp` file into `/var/log` and just use
the system's `last` utility, or run `make check` to list all possible
hacked accounts (only one is the solution).


Tested on Ubuntu 16.04

--
**Pixels Camp 2016 Qualifiers**
