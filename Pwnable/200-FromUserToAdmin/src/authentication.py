import time
import struct
import base64
import crypto

import settings

BOX = crypto.Toolbox(settings.EKEY, settings.AKEY)
MAX_USER_LEN = 12
MAX_TOKEN_LEN = 16
USER_PADDING = '\0'


def generate_token(username, ttl=7200):
    # A token is a base64-encoded, encrypted, binary structure as follows:
    # [padded username (12 bytes)][time to live (4 byte big-endian integer)]
    #
    # Example for username "user":
    # 'user\x00\x00\x00\x00\x00\x00\x00\x00W\xea\xae\xd9'
    # Example for username "admin":
    # 'admin\x00\x00\x00\x00\x00\x00\x00W\xea\xae\xd9'

    until = int(time.time()) + ttl
    until_bytes = struct.pack('>I', until)
    # Truncate user to MAX_USER_LEN bytes
    username = username[:MAX_USER_LEN]
    # Pad it, if required
    delta = MAX_USER_LEN - len(username)
    if delta > 0:
        username += '\0' * delta

    plaintext = username + until_bytes
    ciphertext = BOX.encrypt(plaintext)
    token = base64.urlsafe_b64encode(ciphertext)

    return token


def verify_token(token):
    try:
        ciphertext = base64.urlsafe_b64decode(token)
    except (AttributeError, ValueError, TypeError):
        return None

    plaintext = BOX.decrypt(ciphertext)
    if plaintext is None or len(plaintext) != MAX_TOKEN_LEN:
        return None

    try:
        user, _ = plaintext.split('\0', 1)
    except (AttributeError, ValueError, TypeError):
        return None

    until_bytes = plaintext[-4:]
    try:
        until = struct.unpack('>I', until_bytes)
    except (AttributeError, ValueError, TypeError):
        return None
    else:
        until = until[0]

    now = int(time.time())
    if now < until:
        return user
    else:
        return None
