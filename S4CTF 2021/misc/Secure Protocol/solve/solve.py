#!/usr/bin/env python3

"""
We have to use length extension attack on sha1 with salt3 as the additional data. We can't afford changing salt1. In order to pass the check we can just add "=" as it is a padding character in base64.
"""

import hashpumpy
import requests
import subprocess
from base64 import *
from time import sleep

def get_hash(salt2, salt3, key_length, signature):
    new_hash, new_msg = hashpumpy.hashpump(signature, salt2, salt3, key_length)
    return new_hash, new_msg

def get_s3():
    r = requests.get("http://secure-protocol.peykar.io/s3")
    # if too_many in r.text:
    #     sleep(10)
    #     print("\nSleeping....")
    #     sleep(7)
    #     print("Done\n")
    #     return get_s3()
    return b64decode(r.text.split(" ")[-1]).decode()

salt1 = b"MjFjNGJhZGExNWMwMTEzMzA1ZGJmMGUzMGI4NzU0NGEK"
salt2 = b"bWFydmVs"
signature = "36d997e2648da5472e46db8bdea91f458dc400bc"
too_many = "429 Too Many Requests"

s1 = b64decode(salt1).decode()
s2 = b64decode(salt2).decode()

def get_body(msg_length, s3):
    prefix_len = len(s1) + msg_length
    h3, d = get_hash(s2, s3, prefix_len, signature)
    # print(h3, d)
    s = b64encode(d[:-len(s3)]).decode()
    return {
            "s1": salt1.decode() + "=",
            "s2": s,
            "h": h3    
    }

prev_s3 = None
# for msg_length in range(1, 1000):
# msg_length = int(input(">> "))
msg_length = 1
while True:
    print("Trying, msg_length =", msg_length)
    s3 = get_s3()
    print("s3 =", s3)
    if prev_s3 is not None and prev_s3 != s3:
        msg_length -= 1
        prev_s3 = s3
        continue

    params = get_body(msg_length, s3)
    print("body =", params)
    r = requests.post("http://secure-protocol.peykar.io/msg", data = params)
    print("response code =", r.status_code)
    # if too_many in r.text:
    #     print("\nSleeping....|")
    #     sleep(7)
    #     print("Done\n")
    #     continue
    print(r.text)
    if not "I knew it! You don't have it!" in r.text:
        print(r.text)
        input("continue?")
    msg_length += 1
    prev_s3 = s3

    print("\n" + "*"*75 + "\n")
    sleep(2)

"""
Trying, msg_length = 31
s3 = Salt:7acc2e2d5a721c81259fdb43c35afabf8f849ef2
body = {'s1': 'MjFjNGJhZGExNWMwMTEzMzA1ZGJmMGUzMGI4NzU0NGEK=', 's2': 'bWFydmVsgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACMA==', 'h': 'e2066dc37b6e921aec497136d4475792a6d8134f'}
response code = 200
Wow, you have it! Flag: S4CTF{HasH_4nd_ba5e64_ok_0k_ok}
Wow, you have it! Flag: S4CTF{HasH_4nd_ba5e64_ok_0k_ok}
"""