#!/usr/bin/env python3

from pwn import xor

f = open('flag.png.enc', 'rb').read()
key = xor(f[:9], bytes.fromhex('89504e470d0a1a0a00'))
ff = open('flag_decrypted.png', 'wb')
ff.write(xor(f, key))
ff.close()