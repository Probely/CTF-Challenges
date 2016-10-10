Solution
========

The `create_password()` function uses the current timestamp (in seconds) as the
random seed. Since the files are small and the ransomware knew where to find
them, chances are the password was created within the same second as the first
file was encrypted. This allows recovering the password by passing the first
file's creation/modification time into the `srandom()` function.

The files are encrypted with `ccrypt` as evidenced by their ".cpt" extension.
The answer is contained in `document4.txt`.


    $ stat ransom/document1.txt.cpt  # look for the modification time
    $ date --date="2016-09-16 14:34:18.000000000 +0100" +%s


Pitfalls
--------

Unix timestamps are UTC, but the output of `stat` is human-readable local time.
If the contestant uses an online tool (or something like that) to make the
conversion, they may get bitten by the timezone.
