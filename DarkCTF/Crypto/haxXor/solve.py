from pwn import *

enc = '5552415c2b3525105a4657071b3e0b5f494b034515'
key = '1337hack'

flag = ''
for i in range(0, len(enc)//2):
	flag += xor(chr(int('0x' + enc[2 * i:2 * i + 2], 16)), key[i % len(key)])

print(flag)