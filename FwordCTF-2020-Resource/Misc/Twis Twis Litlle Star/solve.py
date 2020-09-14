from pwn import *
import os

host = 'twistwislittlestar.fword.wtf'
port = 4445

p = remote(host, port)


for i in range(3):
	p.recvuntil('is :')
	num = p.recvline().strip()
	f = open('known.txt', 'a')
	f.write(str(num))
	f.write('\n')
	f.close()

for i in range(624 - 3):
	p.recvuntil('next one : ')
	p.sendline(str(1))
	log.info('Get {}'.format(i))
	p.recvuntil('was : ')
	num = p.recvline().strip()
	f = open('known.txt', 'a')
	f.write(str(num))
	f.write('\n')
	f.close()

log.info("Predicting ...")
os.system('cat known.txt | mt19937predict | head -n 20 > predicted.txt')
log.info("Ready to guessssss ~~~")

f = open('predicted.txt', 'r')
lines = f.readlines()

for line in lines:
	line = line.strip()
	log.info("Ready to solve with: {}".format(line))
	p.recvuntil('next one : ')
	p.sendline(line)

p.interactive()
f.close()
p.close()