import ecdsa
import binascii

from ecdsa import VerifyingKey
from hashlib import sha256
from ecdsa import numbertheory as nt


# On the geth console
# > eth.getRawTransaction("0x83cc2086b2ca5636c865f910ce473c388ed9b92659e5e24b8ca7cb8cb918dd09")
# "0xf86c8085065680769f83015f909412859112a1a5ae0b3cabf1acc9118c6a3d1e5e3d87038d7ea4c680008026a03906ea21a9252cc364b812a82df152d41d2220df4c80def228ce83b0275a411ca02fc8ba753750c3cc19873d125bc26f0d430426d90d05e757f2f8ff603c1d3e80"
#>

# Nodejs
# > var Web3 = require('web3');
# > var web3 = new Web3(new Web3.providers.HttpProvider('http://127.0.0.1:8545'));
# > var util = require('ethereumjs-util');
# > var tx = require('ethereumjs-tx');
# > var ec = require('secp256k1')
# > txn = new tx("0xf86c8085065680769f83015f909412859112a1a5ae0b3cabf1acc9118c6a3d1e5e3d87038d7ea4c680008026a03906ea21a9252cc364b812a82df152d41d2220df4c80def228ce83b0275a411ca02fc8ba753750c3cc19873d125bc26f0d430426d90d05e757f2f8ff603c1d3e80");
# > t.getSenderPublicKey().toString('hex')
# '638f5c8ff99a9366d63072abbbfa25a5eb2b48974f8f05908987581aceb8fc6673ad4558c48b176ad30c9a764e5093fb1a0c8d7ac1f7150a02fcf6fbed7d5d38' (pubkey_hex)
# > txn.r.toString('hex')
# '3906ea21a9252cc364b812a82df152d41d2220df4c80def228ce83b0275a411c' (r_hex)
# > txn.s.toString('hex')
# '2fc8ba753750c3cc19873d125bc26f0d430426d90d05e757f2f8ff603c1d3e80' (s_hex)
# > t.hash(false).toString('hex')
# 'd8a34a11c3abfd8d9ed664977754d1c2cba35881935e1b9cafa4f0e01911257c' (msghash_hex)

pubkey_hex = b'638f5c8ff99a9366d63072abbbfa25a5eb2b48974f8f05908987581aceb8fc6673ad4558c48b176ad30c9a764e5093fb1a0c8d7ac1f7150a02fcf6fbed7d5d38'
msghash_hex = b'd8a34a11c3abfd8d9ed664977754d1c2cba35881935e1b9cafa4f0e01911257c'
r_hex = b'3906ea21a9252cc364b812a82df152d41d2220df4c80def228ce83b0275a411c'
s_hex = b'2fc8ba753750c3cc19873d125bc26f0d430426d90d05e757f2f8ff603c1d3e80'

pubkey_bytes = binascii.unhexlify(pubkey_hex)
pubkey = VerifyingKey.from_string(pubkey_bytes, curve=ecdsa.SECP256k1)
order = pubkey.curve.order

r = int(r_hex, 16)
s = int(s_hex, 16)
z = int(msghash_hex, 16)

print("r: %d, s: %d, z: %d" % (r, s, z))

privkey = None
generator = pubkey.curve.generator
pubkey_point = pubkey.pubkey.point

k_bytes = b'\x00' * 28 + b'four'
k = int.from_bytes(k_bytes, byteorder='big', signed=False) % order
print("k is: 0x%x" % k)

print("Checking that (G * k).x  == r. %d == %d" % ((generator * k).x(), r))
assert((generator * k).x() == r)

for i in range(2):
    privkey_maybe = ((-1**i * s) * k - z)  * nt.inverse_mod(r, order)
    privkey_maybe %= order
    print("pubkey: %s, privkey: %x, G * privkey: %s" % (pubkey_point,
        privkey_maybe, (generator * privkey_maybe)))
    if pubkey_point == generator * privkey_maybe:
        privkey = privkey_maybe
        privkey_bytes = binascii.unhexlify('%x' % privkey)

        sk = ecdsa.SigningKey.from_string(privkey_bytes, curve=ecdsa.SECP256k1)
        print(sk.to_pem().decode())
        hex_privkey = binascii.hexlify(privkey_bytes)
        print('hex private key: %s, hex sha256 private key: %s' %
        (hex_privkey, sha256(hex_privkey).hexdigest()))
        sig = sk.sign(b'message')
        pubkey.verify(sig, b'message')

        break

# Alternative approach: Extract k, without reverse engineering the binary,
# and without doing two signatures
# If we use a known private key, k can be extract directly
# Remember that s can be negative. Try both

inv_s = nt.inverse_mod(s, order)
inv_negative_s = nt.inverse_mod(-s, order)
rda = r * privkey
z_plus_rda = (z + rda) % order

print(hex(inv_s * z_plus_rda))
print(hex((inv_negative_s * z_plus_rda) % order))

