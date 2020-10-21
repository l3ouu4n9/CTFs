from pwn import *

HOST = 'env2.hacktober.io'
PORT = 5000

p = remote(HOST, PORT)
p.recvuntil('spaces.\n')

ret = ''
for i in range(1, 501):
	if i % 3 == 0:
		if i % 5 == 0:
			ret += 'RedRum,'
		else:
			ret += 'Red,'
	elif i % 5 == 0:
		ret += 'Rum,'
	else:
		ret += str(i) + ','
ret = ret[:-1]
p.sendline(ret)
p.interactive()