#!/usr/bin/env python3

crypto = [98,106,115,120,80,75,77,72,124,34,55,78,27,68,4,51,98,93,80,82,25,101,37,127,47,59,23]

for i in range(len(crypto)):
    print(chr(crypto[i] ^ ((i * 9) & 127)), end="")

print()
