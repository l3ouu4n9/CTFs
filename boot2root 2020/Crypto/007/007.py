#!/user/bin/python2
import random
def rot(s, num):
	l=""
	for i in s:
		if(ord(i) in range(97,97+26)):
			l+=chr((ord(i)-97+num)%26+97)
		else:
			l+=i
	return l

def xor(a, b):
	return chr(ord(a)^ord(b))

def encrypt(c):
	cipher = c
	x=random.randint(1,1000)
	for i in range(x):
		cipher = rot(cipher, random.randint(1,26))
	cipher = cipher.encode('base64')

	l = ""
	for i in range(len(cipher)):
		l += xor(cipher[i], cipher[(i+1)%len(cipher)])
	return l.encode('base64')

flag = "#################"
print "cipher =", encrypt(flag)

#OUTPUT: cipher = MRU2FDcePBQlPwAdVXo5ElN3MDwMNURVDCc9PgwPORJTdzATN2wAN28=

