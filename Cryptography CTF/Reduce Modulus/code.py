from Crypto.Util.number import *
import gmpy2
from flag import *
def GenerateKey(length):
        Primes = [getPrime(length) for _ in range(4)]
        modulus = (Primes[0] * Primes[1] * Primes[2] * Primes[3], Primes[0] * Primes[1])
        return modulus

def encrypt(msg, modulus):
    enc = pow(bytes_to_long(msg.encode('utf-8')), 65537, modulus[0] * modulus[1])
    return enc
length = 256
modulus = GenerateKey(length)
print('pubkey =', modulus)
enc = encrypt(secret, modulus)
print('enc =', enc)

