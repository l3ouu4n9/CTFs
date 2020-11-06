from functools import reduce
from binascii import unhexlify

enc = open('enc.txt', 'r').read().strip()
enc = [enc[i:i + 15] for i in range(0, len(enc), 15)]

def correct(enc):
    enc = [int(i) for i in enc]
    pos = reduce(lambda a, b: int(a) ^ int(b), [j + 1 for j, bit in enumerate(enc) if bit])
    enc[pos - 1] = int(not enc[pos - 1])
    enc = ''.join([str(i) for i in enc])
    return enc[2] + enc[4:7] + enc[8:]

flag = ''.join(correct(x) for x in enc)
flag = unhexlify('%x' % int(flag, 2))
print(flag)
