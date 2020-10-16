from Crypto.Util.number import getPrime, isPrime, bytes_to_long
from random import getrandbits
from secret import flag

a = getrandbits(64)
b = getrandbits(64)
e = getPrime(64)
r = []
r.append((a*getrandbits(64)+b)%e)
k = 0
while k<len(flag):
        r.append((a*r[k]+b)%e)
        k+=1

p = getPrime(512)
i = 1
while True:
        q = p + i
        if isPrime(q):
                break
        i += 1
n = p*q
m = bytes_to_long(flag)
c = pow(m,e,n)
obj = open('output.txt','w')
obj.write("r = " + str(r) + "\n")
obj.write("c = " + hex(c) + "\n")
obj.write("n = " + hex(n) + "\n")
obj.close()
