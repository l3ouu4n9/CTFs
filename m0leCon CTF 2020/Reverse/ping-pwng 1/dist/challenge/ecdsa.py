from fastecdsa import ecdsa
from fastecdsa.curve import P256
from fastecdsa.point import Point
from fastecdsa.keys import export_key, gen_keypair
from Crypto.Util.number import bytes_to_long, long_to_bytes
from hashlib import sha256
from os import urandom
from Crypto.Util.number import inverse

def generateKeyPair():
    d, Q = gen_keypair(P256)
    return d, (Q.x, Q.y)

def sign(to_sign, priv):
    r, s = 0, 0
    while r == 0:
        num_to_sign = bytes_to_long(sha256(to_sign).digest())
        k = bytes_to_long(urandom(16))
        X = k * P256.G
        r = X.x
        s = (inverse(k,P256.q)*(num_to_sign+r*priv)) % P256.q
    signature = hex(r)[2:].rjust(64,'0')+hex(s)[2:].rjust(64,'0')
    return bytes.fromhex(signature)

def verify(msg, signature, pub):
    assert P256.is_point_on_curve(pub)
    pub = Point(pub[0], pub[1], curve=P256)
    assert pub != Point.IDENTITY_ELEMENT
    assert P256.q * pub == Point.IDENTITY_ELEMENT
    r, s = bytes_to_long(signature[:32]), bytes_to_long(signature[32:])
    z = bytes_to_long(sha256(msg).digest())
    i = inverse(s,P256.q)
    u1 = (z*i) % P256.q
    u2 = (r*i) % P256.q
    X = u1 * P256.G + u2 * pub
    if X == Point.IDENTITY_ELEMENT:
        return 0
    if X.x == r:
        return 1
    return 0
