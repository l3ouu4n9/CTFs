#!/usr/bin/env python3
from random import SystemRandom
from config import p,q,e,flag

print("="*50)
print(open(__file__).read())
print("~"*50)

random = SystemRandom()

flag = int.from_bytes(flag,"big")

n = p*q
assert(p<q<2*p)

print(f"{n=}")
print(f"{e=}")

def pad(m):
    assert(m<2**128)
    r = random.randrange(2**(p.bit_length()-65))
    return m+r**2

def encrypt(m):
    return pow(pad(m), e, n)

for i in bin(flag)[2:]:
    print(encrypt(int(i)))