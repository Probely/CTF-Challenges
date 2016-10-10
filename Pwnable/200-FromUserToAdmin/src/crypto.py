import hmac
import os

from hashlib import sha256
from Crypto.Cipher import AES


class Toolbox(object):
    '''
    Message encryption and authentication
    '''

    def __init__(self, enc_key, hmac_key, blocksize=16, hashsize=32):
        self.enc_key = enc_key
        self.hmac_key = hmac_key
        self.blocksize = blocksize
        self.hashsize = hashsize

    def is_equal(self, a, b):
        '''
        Constant-time comparison function to avoid cryptographic timing attacks
        '''
        value = bytes(a)
        target = bytes(b)

        delta = len(target) - len(value)
        if delta < 0:
            value = value[:len(target)]
        elif delta > 0:
            value += (b'\x00' * delta)

        result = 0
        for x, y in zip(value, target):
            x = ord(x)
            y = ord(y)
            result |= x ^ y

        return result == 0

    def _pkcs5_pad(self, data):
        padding = self.blocksize - (len(data) % self.blocksize)
        return data + chr(padding) * padding

    def _pkcs5_unpad(self, data):
        padding = ord(data[-1])
        return data[:-padding]

    def _encrypt(self, key, plaintext, iv=''):
        cipher = AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
        ciphertext = cipher.encrypt(self._pkcs5_pad(plaintext))
        return ciphertext

    def _decrypt(self, key, ciphertext, iv=''):
        cipher = AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
        plaintext = cipher.decrypt(ciphertext)
        return self._pkcs5_unpad(plaintext)

    def _authenticate(self, ciphertext):
        hmac_obj = hmac.new(self.hmac_key, digestmod=sha256)
        hmac_obj.update(ciphertext)
        return hmac_obj.digest()

    def _verify_and_strip_hmac(self, message):
        # Message size is at least the authenticator size plus
        # the minimum ciphertext size with padding
        if len(message) < self.hashsize + self.blocksize:
            return None

        msg_hmac = message[:self.hashsize]
        ciphertext = message[self.hashsize:]
        hmac_obj = hmac.new(self.hmac_key, digestmod=sha256)
        hmac_obj.update(ciphertext)
        our_hmac = hmac_obj.digest()

        if self.is_equal(msg_hmac, our_hmac):
            return ciphertext
        else:
            return None

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

    def decrypt(self, ciphertext):
        # Sanity check
        # Expected ciphertext structure:
        #
        # [iv][authenticator][encrypted data]
        #
        # The length of the ciphertext must be at least:
        #   self.blocksize (initialization vector) +
        #   self.hashsize (authenticator) +
        #   self.blocksize (encrypted and padded data)
        expected_len = self.hashsize + self.blocksize * 2
        if len(ciphertext) < expected_len:
            return None

        # Extract initialization vector and ciphertext
        iv = ciphertext[:self.blocksize]
        ciphertext = ciphertext[self.blocksize:]

        # Ensure that the message was not modified
        ciphertext = self._verify_and_strip_hmac(ciphertext)
        if not ciphertext:
            return None

        plaintext = self._decrypt(self.enc_key, ciphertext, iv)

        return plaintext
