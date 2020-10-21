from pwn import *

HOST = 'env2.hacktober.io'
PORT = 5001

p = remote(HOST, PORT)

ret = ''
num = 666
for row in range(1, 31):
	for i in range(row):
		ret += str(num) + ' '
		num += 1

ret = ret[:-1]
p.recvuntil('deal.')
print(ret)
p.sendline(ret)
p.interactive()