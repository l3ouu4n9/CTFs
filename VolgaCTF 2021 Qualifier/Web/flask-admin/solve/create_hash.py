#!/usr/bin/env python3

from werkzeug.security import generate_password_hash

print(generate_password_hash('hacker'))