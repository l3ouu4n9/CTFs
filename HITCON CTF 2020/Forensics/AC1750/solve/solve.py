#!/usr/bin/python3
import json
from Crypto.Cipher import AES
import binascii

f = open('20002.json')

j = json.load(f)
key = '54504f4e454d4553485f4b6621786e3f'
key = binascii.unhexlify(key)
IV = '31323334353637383930616263646566'
IV = binascii.unhexlify(IV)
print(key,IV)
cipher = AES.new(key, AES.MODE_CBC, IV=IV)
flag = ''

for p in j:
    c = p['_source']['layers']['data']['data.data'].replace(":","")[32:]
    if(len(c)%16 == 0): 
        pl = cipher.decrypt(binascii.unhexlify(c))
        flag += pl.split(b'slave_mac')[1][14:15].decode()
print(flag)