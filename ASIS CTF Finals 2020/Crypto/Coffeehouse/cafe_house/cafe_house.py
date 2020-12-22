#!/usr/bin/env python3

import random
from flag import flag

def genkey():
	key = []
	r, s = random.randint(1, 1<<16), random.randint(1, 1<<16)
	return [r, s, r ^ s, r & s]

def encrypt(u, v, key, d):
	assert u < 2**16 and v < 2**16
	s = 0
	for i in range(32):
		s = (s + d) % 2**16
		w = ((v<<4) + key[0]) ^ (v + s) ^ ((v>>5) + key[1]) % 2**16
		u = (u + w) % 2**16
		x = ((u<<4) + key[2]) ^ (u + s) ^ ((u>>5) + key[3]) % 2**16
		v = (v + x) % 2**16
	return (u, v)

d = 0xf00d
key = genkey()
msg = [flag[4*i:4*(i+1)] for i in range(len(flag) // 4)]
enc = []
for i in range(len(msg)):
	u, v = int(msg[i][:2].encode("utf-8").hex(), 16), int(msg[i][2:].encode("utf-8").hex(), 16)
	c_1, c_2 = encrypt(u, v, key, d)
	enc += [c_1] + [c_2]

print('key =', '?')
print('enc =', enc)

