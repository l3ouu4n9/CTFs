#!/usr/bin/env python3

from Crypto.Util.number import *

with open('zwsp.txt', 'rb') as f:
    data = f.read()

i = 0
curr = []

bin_string = ''

for char in data:
    if char not in b'Pretty empty over here':
        i += 1
        curr.append(char)
        if i % 3 == 0:
            i = 0
            print(curr)

            if curr[-1] == 139:
                bin_string += '0'
            else:
                bin_string += '1'

            curr = []

print(bin_string)
print(int(bin_string, 2))
print(long_to_bytes(int(bin_string, 2)))