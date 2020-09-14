from pwn import *
import hashlib

def find_md5sum(target):
	length = len(target)
	for i in range(1000 ** 6):
		m = hashlib.md5()
		m.update(str(i))
		h = m.hexdigest()
		if h[0:length] == target:
			return str(i)

def find_sha1sum(target):
	length = len(target)
	for i in range(1000 ** 6):
		s = hashlib.sha1()
		s.update(str(i))
		h = s.hexdigest()
		if h[0:length] == target:
			return str(i)

p = remote('jh2i.com', 50005)
r = 'Correct'
while 'Correct' in r:
	data = p.recvuntil('\n').split()
	if ('Enter' not in data) or (len(data) < 15):
		print(' '.join(data))
		break
	protocol = data[10]
	target = data[14]
	print(protocol, target)

	if protocol == 'md5sum':
		payload = find_md5sum(target)
	else:
		payload = find_sha1sum(target)

	p.sendline(payload)
	r = p.recvuntil('\n')
	print(r)

p.close()

