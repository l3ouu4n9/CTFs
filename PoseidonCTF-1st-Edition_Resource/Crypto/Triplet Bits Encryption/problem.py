#!/usr/bin/env python3

from hashlib import sha256
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Random import get_random_bytes
from flag import flag

def mixkeybit(keybit1, keybit2, keybit3):
    return int(keybit1 or (not(keybit2) and keybit3))

key1 = get_random_bytes(32)
key2 = get_random_bytes(32)
key3 = get_random_bytes(32)

wfile = open('output.txt', 'w')

for _ in range(256):
    flagbin = bin(bytes_to_long(flag))[2:]
    encbin = ""
    for i in range(len(flagbin)):
        key1 = sha256(key1).digest()
        key2 = sha256(key2).digest()
        key3 = sha256(key3).digest()
        keybit1 = int(bin(bytes_to_long(key1))[2:][-1])
        keybit2 = int(bin(bytes_to_long(key2))[2:][-1])
        keybit3 = int(bin(bytes_to_long(key3))[2:][-1])
        encbin += str(mixkeybit(keybit1, keybit2, keybit3) ^ int(flagbin[i]))
    wfile.write(encbin)
    wfile.write('\n')
wfile.close()
