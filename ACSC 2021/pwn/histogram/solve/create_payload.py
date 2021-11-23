#!/usr/bin/env python

payload = "-nan, 101.0\n"
f = open("payload.csv", "w")
for i in range(456):
    f.write(payload)
f.write("inf, inf")
f.close()
