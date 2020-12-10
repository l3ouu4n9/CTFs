#!/usr/bin/env python3
from Crypto.Cipher import AES
import base64,random,hashlib,json,string
import time
from secret import *

class MyRandom:
    def __init__(self):
        self.mask = (1<<64)-1
        self.offset = 0
        self.magic = random.getrandbits(64)
        self.state = random.getrandbits(64)

    def __iter__(self):
        return self

    def __next__(self):
        self.state = (self.state * self.state) & self.mask
        self.offset = (self.offset + self.magic) & self.mask
        self.state = (self.state + self.offset) & self.mask
        self.state = ((self.state << 32) | (self.state >> 32)) & self.mask
        return self.state >> 32


def get_random(my_random, b):
    b //= 4
    lst = [next(my_random) for i in range(b)]
    byte_lst = []
    for v in lst:
        byte_lst.append(v%256)
        byte_lst.append((v>>8)%256)
        byte_lst.append((v>>16)%256)
        byte_lst.append((v>>24)%256)
    return bytes(byte_lst)

def pad(s):
    pad_len = 16-len(s)%16
    return s+chr(pad_len)*pad_len

def unpad(s):
    v = ord(s[-1])
    assert(s[-v:] == chr(v)*v)
    return s[:-v]

def proof_of_work():
    proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(20)])
    digest = hashlib.sha256(proof.encode()).hexdigest()
    print("SHA256(XXXX+%s) == %s" % (proof[4:],digest))
    x = input('Give me XXXX:')
    if len(x)!=4 or hashlib.sha256((x+proof[4:]).encode()).hexdigest() != digest: 
        exit()

if __name__ == '__main__':
    key = open('key','rb').read()
    flag = user_secret+admin_secret
    assert(flag.startswith('hitcon{'))
    assert(flag.endswith('}'))
    assert(len(user_secret)==16)
    assert(len(admin_secret)==16)
    proof_of_work()
    my_random = MyRandom()
    iv =  get_random(my_random, 16)
    note = {}
    while True:
        try:
            msg = input("cmd: ")
            if msg == "register":
                name = input("name: ")
                if name == 'admin':
                    print('no! I dont believe that')
                    exit()
                data = {'secret': user_secret, 'who': 'user', "name": name}
                string = json.dumps(data)
                cipher = AES.new(key, AES.MODE_CBC, iv)
                encrypted = cipher.encrypt(pad(string).encode()).hex()
                send_data = {"cipher": encrypted}
                print("token: ",base64.b64encode(json.dumps(send_data).encode()).decode())
            elif msg == "login":
                recv_data = json.loads(base64.b64decode(input("token: ").encode()).decode())
                if 'iv' in recv_data:
                    iv = bytes.fromhex(recv_data['iv'])
                encrypted = bytes.fromhex(recv_data['cipher'])
                cipher = AES.new(key, AES.MODE_CBC, iv)
                string = unpad(cipher.decrypt(encrypted).decode())
                data = json.loads(string)
                if 'cmd' in data:
                    if data['cmd'] == 'get_secret':
                        if "who" in data and data["who"] == "admin" and data["name"] == 'admin':
                            data["secret"] = admin_secret
                    elif data['cmd'] == 'get_time':
                        data['time'] = str(time.time())
                    elif data['cmd'] == 'note':
                        note_name = get_random(my_random, 4).hex() 
                        note[note_name] = data['note']
                        data['note_name'] = note_name
                    elif data['cmd'] == 'read_note':
                        note_name = data['note_name'] 
                        data['note'] = note[note_name]
                string = json.dumps(data)
                cipher = AES.new(key, AES.MODE_CBC, iv)
                encrypted = cipher.encrypt(pad(string).encode()).hex()
                send_data = {"cipher": encrypted}
                print("token: ",base64.b64encode(json.dumps(send_data).encode()).decode())
        except Exception as e:
            exit()

