from Crypto.Util.number import *
import gmpy2
import random

length_bit = 4096
def generate_key(length_bit = 4096):
	q = getPrime(length_bit)
	f = random.getrandbits(length_bit/2)
	while True:
		g = random.getrandbits(length_bit*3/8)
		if gmpy2.gcd(f,g) == 1:
			break
	h = gmpy2.invert(f, q)*g % q
	return h,q,f,g

def encrypt(m,h,q):
	m = bytes_to_long(m)
	r = random.getrandbits(length_bit/2)
	enc = (r*h + m) % q
	return long_to_bytes(enc)
def decrypt(enc,f,g,h,q):
	a = f*enc % q
	b = gmpy2.invert(f,g)*a % g
	return long_to_bytes(b)

h,q,f,g = generate_key()
pub = open("public.key","w")
pub.write(str(h)+"\n")
pub.write(str(q))
pub.close()

priv = open("priv.key","w")
priv.write(str(f)+"\n")
priv.write(str(g))
priv.close()

flag = "############"
enc = open("enc","wb")
enc.write(encrypt(flag,h,q))
enc.close()


