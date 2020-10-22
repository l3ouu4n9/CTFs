from Crypto.Util.number import *
import numpy as np

mark = 3**66

def get_random_prime():
    total = 0
    for i in range(5):
        total += mark**i * getRandomNBitInteger(32)
    fac = str(factor(total)).split(" * ")
    return int(fac[-1])

def get_B(size):
    x = np.random.normal(0, 16, size)
    return np.rint(x)

p = get_random_prime()
q = get_random_prime()
N = p * q
e = 127

flag = b"N1CTF{************************************}"
secret = np.array(list(flag))

upper = 152989197224467
A = np.random.randint(281474976710655, size=(e, 43))
B = get_B(size=e).astype(np.int64)
linear = (A.dot(secret) + B) % upper

result = []
for l in linear:
    result.append(pow(l, e, N))

print(result)
print(N)
np.save("A.npy", A)
