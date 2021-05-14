#!/usr/bin/python
import socket
import struct

# nstftp://umbccd.io:4300/

class STFTPClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.sock.connect(("umbccd.io", 4300))
        print(self.__recvmsg__()[1])
        self.__sendmsg__(2, b"@<")

    def __sendmsg__(self, command, buf):
        packed_data = buf
        tosend = struct.pack("<BQB", command, len(buf)+10, len(packed_data))
        print((tosend + packed_data)[0xa:])
        self.sock.send(tosend + packed_data)
    
    def __recvmsg__(self, no_decode=False):
        buf = self.sock.recv(9)
        cmd, len = struct.unpack("<BQ", buf)
        data = self.sock.recv(len - 9)
        if no_decode:
            return data
        return data[1:]
    
    def listfiles(self, dir):
        self.__sendmsg__(3, bytes(dir, "ascii"))
        buf = self.__recvmsg__()
        while buf != b"":
            print(buf)
            buf = self.__recvmsg__()
    
    def recvfile(self, path):
        self.__sendmsg__(5, bytes(path, "ascii"))
        filelen = self.__recvmsg__(True)
        filelen = struct.unpack("<Q", filelen)[0]
        buf = b""
        while filelen > len(buf):
            buf += self.sock.recv(4096)
        return buf

client = STFTPClient()
client.listfiles(".")
file = open("libc-2.31.so", "wb")
file.write(client.recvfile("libc-2.31.so"))
file.close()
for _ in range(7):
    client.recvfile("README.txt")
    
client.__sendmsg__(7, b"@@")
print(client.__recvmsg__())
client.__sendmsg__(9, b"UMBCDAWG")
print(client.__recvmsg__())

"""
83
b'@<'
b'.'
b'.bashrc'
b'.profile'
b'.'
b'.bash_logout'
b'..'
b'flag_printer'
b'libc-2.31.so'
b'README.txt'
b'nstftp'
b'libc-2.31.so'
b'README.txt'
b'README.txt'
b'README.txt'
b'README.txt'
b'README.txt'
b'README.txt'
b'README.txt'
b'@@'
b'\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00@<'
b'UMBCDAWG'
b'DawgCTF{pr0t0c0l5_ar3_fun_but_n0t_tr1v1@l}'
"""