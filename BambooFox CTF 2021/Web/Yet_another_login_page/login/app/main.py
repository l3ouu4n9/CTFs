#!/usr/bin/env python3
from os import getenv, urandom
from flask import Flask, g, request, session, send_file
import sqlite3
import secrets

app = Flask(__name__)


@app.route('/hey_guys_this_is_the_flag_route')
def get_flag():
    magic = [247, 254, 216, 225, 234, 243, 216, 244, 243, 245, 216, 228, 232, 232, 235, 166, 184]
    keys = [request.args.get("give"), request.args.get("me"), request.args.get("flag")]
    if keys[0] == str(magic[3]) and keys[1] == str(magic[-3]) and keys[2] == "\x87":
        return "flag{"+''.join(map(lambda n: chr(n ^ ord(keys[2])), magic))+"}"
    return "NO FLAG FOR YOU"


class User():
    def __init__(self, username, ip):
        self.username = username
        self.ip = ip


def db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('/tmp/db.sqlite3')
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.before_first_request
def server_start():
    cursor = db().cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS "users" (
        "username"  TEXT NOT NULL,
        "password"  TEXT NOT NULL
    )
    ''')
    cursor.execute("SELECT COUNT(*) as count FROM users WHERE username='admin'")
    count = cursor.fetchone()['count']
    if count == 0:
        cursor.execute("INSERT INTO users (username, password) VALUES (?,?)",
                       ('admin', secrets.token_urlsafe()))
    db().commit()


@app.route('/')
def index():
    return send_file("index.html")


@app.route('/login', methods=["POST"])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    user = User(username, request.remote_addr)

    cursor = db().cursor()
    cursor.execute(f"select username, password from users where username='{username}'")
    res = cursor.fetchone()

    if res:
        if res['password'] == password:
            return f"Hello {res['username']} ｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡"
        else:
            return ("Wrong password for " + res['username'] + ", login from {0.ip}.").format(user)
    else:
        return "User not found!"


if __name__ == "__main__":
    app.run(port=3000, debug=True)
