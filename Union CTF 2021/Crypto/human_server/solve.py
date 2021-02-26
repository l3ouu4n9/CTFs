#!/usr/bin/env python3

import json, hashlib

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import getPrime, long_to_bytes

from fastecdsa.curve import secp256k1
from fastecdsa.point import Point

CURVE = secp256k1
ORDER = CURVE.q
G = CURVE.G

DUMMY_NONCE = 2**65

alice_pub = json.loads(input('alice.pub?'))
print('{"Px": %d, "Py": %d, "nonce": %d}' % (G.x, G.y, DUMMY_NONCE))

bob_pub = json.loads(input('bob.pub?'))
shared_secret = bob_pub['Px'] ^ DUMMY_NONCE
alice_nonce = bob_pub['Px'] ^ alice_pub['Px'] ^ DUMMY_NONCE
print('{"Px": %d, "Py": %d, "nonce": %d}' % (G.x, G.y, alice_nonce))

aes_key = hashlib.sha1(long_to_bytes(shared_secret)).digest()[:16]
aes_data = json.loads(input('aes.data?'))
aes_iv = bytes.fromhex(aes_data['iv'])
cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
ciphertext = bytes.fromhex(aes_data['encrypted_flag'])
print(cipher.decrypt(ciphertext))

# union{https://buttondown.email/cryptography-dispatches/archive/cryptography-dispatches-the-most-backdoor-looking/}