from pwn import *

host = 'secretarray.fword.wtf'
port = 1337

p = remote(host, port)

p.recvuntil('START:\n')

num_array = []
sum_array = []
for i in range(1337):
	payload = '{} {}'.format(i, (i + 1) % 1337)
	p.sendline(payload)
	num = int(p.recvline())
	log.info("Get {}".format(i))
	sum_array.append(num)
	
A_mul_2 = 0
for i in range(1337):
	A_mul_2 += (sum_array[i] * ((-1) ** i))

A = A_mul_2 / 2
num_array.append(A)

payload = 'DONE'
for i in range(1337):
	num_array.append(sum_array[i] - num_array[i % 1336])
	payload += ' {}'.format(num_array[i])


p.sendline(payload)
print(p.recvline())
p.close()
