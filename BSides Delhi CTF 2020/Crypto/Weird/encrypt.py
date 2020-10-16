from Crypto.Util.number import getPrime, getRandomRange, bytes_to_long, inverse
from gmpy2 import gcd, lcm
from flag import flag
def keygen():
	p = getPrime(512)
	q = getPrime(512)
	n = p*q
	g = getRandomRange(0,pow(n,2))
	return (g, n)

def encrypt(message, publickey, g):
	r = getRandomRange(0,publickey)
	assert gcd(r,publickey) == 1
	m1 = pow(g,int(message),pow(publickey,2))*pow(r,publickey,pow(publickey,2))
	c = m1 % pow(publickey,2)
	return c
	
f = open('output.txt','w')
pubkey = keygen()
ciphertexts = []
for i in flag:	
	ciphertexts.append(encrypt(i, pubkey[1], pubkey[0]))
f.write('g = ' + str(pubkey[0]) + '\n')
f.write('n = ' + str(pubkey[1]) + '\n')
f.write('c = ' + str(ciphertexts) + '\n')
f.close()
