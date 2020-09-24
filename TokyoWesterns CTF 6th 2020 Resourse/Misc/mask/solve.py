#!/usr/bin/python3

import ipaddress
import base64

f = open('ips.txt', 'r')

flag_b64 = ''
for line in f:
    line = line.strip().split('/')
    flag_b64 += chr(int(ipaddress.ip_address(line[0])) - (int(ipaddress.ip_address(line[0])) & int(ipaddress.ip_address(line[1]))))

print(base64.b64decode(flag_b64))