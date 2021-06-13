#!/usr/bin/env python3

from flask import Flask,request
import os


app = Flask(__name__)


@app.route('/')
def handle():
    global flag
    ch = request.args.get('c')
    print(ch)
    flag += ch
    return ch

@app.route('/get_flag')
def getter():
    global flag
    return flag

if __name__ == '__main__':
    global flag
    flag = 'z'
    app.run(host='0.0.0.0', port=9002)