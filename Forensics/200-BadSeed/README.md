F200 - Bad Seed
===============

Our client has been the victim of a previously unknown ransomware, seemingly
targeted specifically at him, as it only encrypted a few known critical files.
We've already looked into the ransomware binary and made sense of the password
generation function.

Can you help?

The C source code for the `create_password()` function is provided along with a
".tar" file containing the client's encrypted files (four files).


Testing
=======

Create the files by running `make`. Make `ransom.tar` available to
contestants. It contains `ransom.c` and the four encrypted files.

Requirements:

    $ apt-get install fortune-mod fortunes ccrypt


Notes
=====

Turns out `srand()`/`rand()` gives different results across platforms, but
`srandom()`/`random()` seems to be consistent. At least between Ubuntu 16.04 x64
and MacOS X 10.11 (El Capitan).


--
**Pixels Camp 2016** - Carlos Rodrigues
