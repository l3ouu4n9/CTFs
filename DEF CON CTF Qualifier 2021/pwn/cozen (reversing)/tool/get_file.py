#!/usr/bin/env python3

from pwn import remote
from itertools import product
import re

HOST, PORT = 'cozen.challenges.ooo', 51015

io = remote(HOST, PORT)

files = [
    [2, range(1,10)],
    [3, range(1,10)],
    [5, range(1,3)],
    [6, 7],
]
files = [ [3, range(1,10)] ]
folder = {
    2: 'games',
    3: 'lib-cozen',
    5: 'utils',
}

io.sendline()
io.sendline()
io.sendline('yay')
io.sendline('y')
io.sendline('yay')
io.sendline('e')
io.sendline('f')

for path in files:
    fn = 'files/'
    if len(path) == 2 and type(path[1]) != int:
        io.sendline(str(path[0]))
        fn += folder[path[0]] + '/'
        path = path[1]
    for _ in range(5):
        for x in path:
            io.sendline(str(x))
            io.readuntil('Sending')
            line = io.readline().decode()
            size,name = re.findall('(\d+) raw bytes for (.+)\n', line)[0]
            binary = io.readuntil("==DONE==")
            md5 = io.readline().decode().strip()
            print(fn, name, size, md5)
            with open(fn+name,'wb') as f:
                f.write(binary)
        io.sendline('n')

io.interactive()
