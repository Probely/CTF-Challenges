Solution
------

This challenge is a pratical example showing that subtly broken cryptography can result in "catastrophic" failure. In this particular example, transforming a 'user' token into an 'admin' token.

The first step is to find out that there is a ```.git``` folder on the root of the service. Use ```DVCS-Pillage``` to extract the repository.

This git repository will have the service source code:
```bash
app.py
authentication.py
crypto.py
```

The ```authentication.py``` file documents the basic token structure.

```python
    # A token is a base64-encoded, encrypted, binary structure as follows:
    # [padded username (12 bytes)][time to live (4 byte big-endian integer)]
    #
    # Example for username "user":
    # 'user\x00\x00\x00\x00\x00\x00\x00\x00W\xea\xae\xd9'
    # Example for username "admin":
    # 'admin\x00\x00\x00\x00\x00\x00\x00W\xea\xae\xd9'
    
    (...)

    ciphertext = BOX.encrypt(plaintext)
```

The ```crypto.py``` file provides a ```Toolbox``` class with encryption and decryption methods.

Inspecting this file will show that the ```encrypt``` method has some interesting comments:

```python
    def encrypt(self, plaintext):
        plaintext = bytes(plaintext)
        # Fetch an iv from /dev/urandom, as recommended by best practices
        iv = os.urandom(self.blocksize)
        # Encrypt the plaintext
        ciphertext = self._encrypt(self.enc_key, plaintext, iv)
        # MAC the ciphertext to make sure nobody messes with it
        authenticator = self._authenticate(ciphertext)

        # XXX: should we also authenticate the iv? I think it should be ok
        # TODO: check crypto.stackexchange to see if this is so
        return iv + authenticator + ciphertext
```

The ```XXX:``` and ```TODO:``` comments provide strong hints that the ```iv``` should be in fact part of the MAC. Failing to do so, specially in CBC mode, will result in some very nasty problems. If we google "crypto.stackexchange authenticate iv", a cryptographic stack exchange page will provide additional [details on the issue](http://crypto.stackexchange.com/questions/24353/encrypt-then-mac-do-i-need-to-authenticate-the-iv).

So, how do we exploit this? How do we transform a 'user' token into an 'admin' token?

Recall that CBC mode works by decrypting a block and xoring it with the previous one, or with the iv if we are decrypting the first block.

We know that the resulting plaintext will be something like:
```python
'user\x00\x00\x00\x00\x00\x00\x00\x00[TTTT]'
```

Where ```[TTTT]``` are the four bytes of the "time to live" field. We do not need to know this value (even though it is guessable).

We wish for it to become:
```python
'admin\x00\x00\x00\x00\x00\x00\x00[TTTT]'
```

What we need to do is manipulate the ```iv``` (remember that it is not authenticated!) in a way that, by exploiting the CBC mechanics, the resulting plaintext will be a valid 'admin' token.

Steps:

```python
# Start by decoding the token
token = base64.urlsafe_b64decode(b64_token)
# The iv is in the first 16 bytes
iv = token[:16]

# We only wish to change the beggining of the token (user->admin). Focus on that:

# Remove the original iv bytes after decryption 
new_iv = iv[:5]
# Remove the original 'user' value
new_iv = xor(new_iv, 'user') 
# Add the 'admin' value
new_iv = xor(new_iv, 'admin')
# Build the final iv. The first 5 bytes are manipulated to make sure that the token
# will be an 'admin' token. The remaining bytes stay unchanged.
new_iv = new_iv + iv[5:]

new_token = new_iv + token[16:]
new_b64_token = base64.urlsafe_b64encode(new_token)
```

Submit ```new_b64_token``` and you should have admin privileges.

