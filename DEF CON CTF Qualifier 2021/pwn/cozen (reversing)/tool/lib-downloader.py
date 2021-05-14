#!/usr/bin/env python3
from pwn import *
import random
import string
import hashlib

letters = string.ascii_letters

def entry():
    p.sendlineafter(b'secure mode?', 'N')
    p.sendlineafter(b'compression?', 'N')
    p.sendlineafter(b'Username:', name)
    p.sendlineafter(b'create new user [Y/n]?', 'Y')
    p.sendlineafter(b'Password:', 'abcd1234')
    p.sendlineafter(b'Show Colors?', 'N')
    p.sendlineafter(b'[C]ontinue', 'C')

def FileArea():
    p.sendlineafter(b'Command >>', 'F')

def download_or_dir(idx=None, next=None, download=None, debug=None):
    if next != None:
        p.sendlineafter(b'[U]pload or File to download >>', 'N')
        return
    p.sendlineafter(b'[U]pload or File to download >>', str(idx))
    if download != None:
        p.recvuntil(b'Sending ')
        size = int(p.recvuntil(b' raw bytes for ', drop=True))
        filename = p.recvline()[:-1]
        content = b''
        waiting_size = size
        while True:
            part = p.recv(waiting_size)
            content += part
            waiting_size -= len(part)
            if waiting_size <= 0:
                break
        p.recvuntil(b'MD5 ')
        md5 = p.recvline()[:-1]
        result_md5 = hashlib.md5(content)
        log.info(b'filename: ' + filename)
        # log.info('size: ' + str(size))
        # log.info('real size: ' + str(len(content)))
        # log.info(b'md5: ' + md5)
        # log.info('md5: ' + result_md5.hexdigest())
        if md5.decode().lower() == result_md5.hexdigest():
            log.info(b'md5 check: ok')
        else:
            log.info(b'md5 check: fail')
        with open(filename.decode(), 'wb') as f:
            f.write(content)
    if debug != None:
        log.info(p.recvuntil(b'raw bytes for '))
        log.info(p.recvline())
        content = p.recvuntil(b'MD5 ')
        content += p.recvline()
        # log.info(content)

p = remote('cozen.challenges.ooo', 51015)
name = ''.join(random.choice(letters) for i in range(10))
log.info('name: ' + name)

entry()

FileArea()

download_or_dir(3)
download_or_dir(6, download=b'Y')
download_or_dir(7, download=b'Y')
download_or_dir(3)
for i in range(0, 38):
    download_or_dir((i % 9) + 1, download=b'Y')
    if (i % 9) == 8:
        download_or_dir(next=b'Y')


# p.interactive()
