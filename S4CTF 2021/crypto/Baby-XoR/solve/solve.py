#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import xor

encrypted_flag = open('flag.enc', 'rb').read()

shift = None
for i in range(len(encrypted_flag)):
    key = b'S4CTF{'
    xored = xor(encrypted_flag[i:i+6], b'S4CTF{')
    if b'S4CTF' in xored:
        shift = i + xored.index(b'S4CTF')

decrypted_flag = [i for i in b'\xff' * shift + b'S4CTF{' + b'\xff' * (len(encrypted_flag) - 6 - shift)]

for i in range(shift, len(encrypted_flag)):
    j = i + 1 if i < len(decrypted_flag) - 1 else 0
    decrypted_flag[j] = decrypted_flag[i] ^ encrypted_flag[i]

print(''.join(chr(i) for i in decrypted_flag))