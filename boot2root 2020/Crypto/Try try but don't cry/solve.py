import base64

with open('chall.txt') as f:
  d = f.read()

for i in range(20):
  if len(d) == 11:
    break
  try:
    d = d.decode('hex')
  except:
    c = len(d) % 4
    for _ in range(c):
      d += b'='
    d = base64.b64decode(d)
#print(d, len(d))

plaintext = 'b00t2root{'
s = '\x03^D\x15A\x06\x06\x0c\x17\x18\x1b'

o = ''
for idx in range(10):
  o += chr(ord(s[idx]) ^ ord(plaintext[idx]))
o += '}'

plaintext += chr(ord(o[-1]) ^ ord(s[-1]))
flag = plaintext + o
print(flag)