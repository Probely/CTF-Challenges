#!/usr/bin/env python3

import requests
import base64
from urllib.parse import urljoin

host = "http://p200-a047ec9117d7e818.ctf.pixels.camp/"

def bxor(b1, b2):
    result = bytearray(b1)
    for i, b in enumerate(b2):
        result[i] ^= b
    return bytes(result)


response = requests.get(urljoin(host, 'token'))
b64_token = response.json()['token']
token = bytearray(base64.urlsafe_b64decode(b64_token))

iv = token[:16]
hmac = token[16:16+32]
ciphertext = token[16+32:]

new_iv = bxor(token[:5], b'user')
new_iv = bxor(new_iv[:5], b'admin')

new_token = base64.urlsafe_b64encode(new_iv + token[5:])
response = requests.get(urljoin(host, 'flag'),
                        headers={'X-API-Token': new_token})
print(response.content.decode())

