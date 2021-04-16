from Crypto.Util.number import *
import random
from s3cr3t import flag, key


def encrypt(m,pub_key):
	c = []
	bin_msg = bin(bytes_to_long(m))[2:]
	n,y = key
	for i in bin_msg:
		x = random.getrandbits(100)
		if (i == '1'):
			c.append((y*pow(x,5,n))%n)
		else:
			c.append(pow(x,5,n))
	return c

ciphertext = encrypt(flag,key)
f = open('ciphertext.txt','w')
f.write(str(ciphertext))

#n = 839647959743379757835423741637185376972991646369
