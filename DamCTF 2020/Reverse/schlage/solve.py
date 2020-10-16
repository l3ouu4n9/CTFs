from pwn import *
import subprocess

elf = ELF('./schlage')
host = 'chals.damctf.xyz'
port = 31932

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([elf.path] + argv, gdbscript=gdbscript, *a, **kw)
        #return gdb.debug([elf.path] + argv, env={"LD_PRELOAD": libc.path}, gdbscript=gdbscript, *a, **kw)
    else:
        return process([elf.path] + argv, *a, **kw)
        #return process([ld.path, elf.path] + argv, env={"LD_PRELOAD": libc.path}, *a, **kw)

def remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
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
b main
continue
'''.format(**locals())

# -- Exploit goes here --
out = ''
while 'Such a cool sentence!' not in out:
	sleep(1)
	p = start()

	#p = process('./schlage')

	# Pin 3
	p.recvuntil('Which pin would you like to open?')
	p.sendline('3')
	p.recvuntil('Give me a number!\n')
	payload = str(0xdeadbeef ^ 322376503)
	p.sendline(payload)
	p.recvuntil('Great!')

	# Pin 1
	p.recvuntil('Which pin would you like to open?')
	p.sendline('1')
	p.recvuntil('Number please!\n')
	payload = str(-18 ^ 62 ^ 87 ^ -127 ^ -45 ^ 37 ^ -109)
	p.sendline(payload)
	p.recvuntil('Great!')

	# Pin 5
	p.recvuntil('Which pin would you like to open?')
	p.sendline('5')
	p.recvuntil('I bet you can\'t guess my random number!\n')
	payload = subprocess.check_output(['./rand_num', '5'])
	p.sendline(payload)
	p.recvuntil('Wow! That was some impressive guessing.')

	# Pin 2
	p.recvuntil('Which pin would you like to open?')
	p.sendline('2')
	p.recvuntil('I wonder what it means?\n')
	seed = p.recvline().strip()
	payload = subprocess.check_output(['./rand_num', '2', seed])
	p.sendline(payload)
	p.recvuntil('Woah, that\'s the lock\'s favorite number too! Small world, eh?')

	# Pin 4
	p.recvuntil('Which pin would you like to open?')
	p.sendline('4')
	p.recvuntil('What\'s your favorite sentence?\n')
	num = int(subprocess.check_output(['./rand_num', '4', seed])) % 10 + 65

	# If num = 67, work
	print(num)
	payload = 'zzzzzE'
	p.sendline(payload)
	out = p.recvline()

# Get Flag
p.recvuntil('Here, have a flag for your troubles:\n')
print(p.recvline())