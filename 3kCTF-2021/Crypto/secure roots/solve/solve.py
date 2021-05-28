from pwn import process, remote
import hashlib
from Crypto.Util.number import long_to_bytes, inverse, GCD

def xgcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = xgcd(b % a, a)
        return (g, x - (b // a) * y, y)

def decrypt(c):
    mp = pow(c, (p+1)//4, p)
    mq = pow(c, (q+1)//4, q)
    _, yp, yq = xgcd(p, q)
    r1 = (yp * p * mq + yq * q * mp) % n
    r2 = n - r1
    r3 = (yp * p * mq - yq* q *mp ) %n
    r4 = n - r3
    return [r1, r2, r3, r4]

def sign(m):
    u = 0
    while True:
        c = int(hashlib.sha256(m+long_to_bytes(u)).hexdigest(), 16)
        rs = decrypt(c)
        for r in rs:
            if c == pow(r, 2, n):
                return r, u
        u += 1

while True:
    #rem = process(['python3','app.py'])
    rem = remote("secureroots.2021.3k.ctf.to", 13371)
    rem.recvuntil("modulus : ")
    n = int(rem.recvline().decode())

    rem.recvuntil("r : ")
    r = int(rem.recvline().decode())
    rem.recvuntil("u : ")
    u = int(rem.recvline().decode())

    U = long_to_bytes(u)
    m = int(hashlib.sha256(b"Guest" + U).hexdigest(), 16)

    if m == pow(r, 2, n):
        print("Correct Signature :( Abort")
        continue

    p = (GCD(pow(r, 2, n) - m , n))
    if p == 1:
        p = GCD(pow(r, 2, n) + m , n)
    q = n//p
    if p == 1:
        continue
    assert p*q == n
    phi = n - p - q + 1 
    d = inverse(0x10001, phi)

    r, u = sign(b"3k-admin")
    if r == None:
        print ("No sigs")
        continue
    print (r)

    rem.recvuntil("Username : ")
    rem.sendline("3k-admin")
    rem.recvuntil("r : ")
    rem.sendline(str(r))
    rem.recvuntil("u : ")
    rem.sendline(str(u))
    rem.recvuntil("Message : ")
    c = int(rem.recvline().decode())
    flag =  long_to_bytes(pow(c, d, n))
    print (flag.decode())
    exit()

    # CTF{f4ulty_s1gn4ture_f41l}