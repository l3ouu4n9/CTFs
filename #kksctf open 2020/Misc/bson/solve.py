#!/bin/env/python3

key = 92
flag = [55,55,47,39,54,47,108,50,3,53,47,3,63,108,108,48,3,62,41,40,
        3,52,61,42,111,3,37,51,41,3,40,46,53,57,56,3,49,111,47,47,
        28,59,57,3,44,61,63,55,33]
ascii_flag = []

for item in flag:
    xor_result = key^item
    ascii_flag.append(chr(xor_result))

for item in ascii_flag: print(item, end="")