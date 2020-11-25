import random
import sys
import time

ct = str(time.time()).encode('ASCII')
random.seed(ct)
flag = 'data_here'.encode('ASCII')
k1 = [random.randrange(256) for _ in flag]
ciphertext = [m ^ k for (m,k ) in zip(flag + ct, k1 + [0x99]*len(ct))]

with open(sys.argv[1], "wb") as f:
    f.write(bytes(ciphertext))
