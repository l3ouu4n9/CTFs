---
layout: post
category: crypto
title: replyCTF 2020 - darth stuff
tags: 
    - rixxc
---

# Overview

The task specifies a server and two tcp ports. Upon connecting to one of the ports we are presented with two hex numbers. After that we have to respond with a number as well.

After we provide a number, the server responds with the string "CFB" and two base64 encoded bytestrings.

# Exploitation

After reconnecting to the server I recognized that the first number called p always stays the same while the second number changes.

Because of the many 0xff bytes at the start and end of the number p I recognized it as one of the standardized (RFC 3526) prime numbers used for the Diffie–Hellman key exchange. Therefore I assumed we had to exchange a key using DH and that the data sent afterwards is the flag encrypted with the shared secret.

The cipher turned out to be AES in CFB mode. The first value is the IV and the second one is the encrypted flag.

This had to be done on both provided ports to get both halves of the flag.

```python
from pwn import *
from Crypto.Cipher import AES
import base64

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


r = remote('gamebox1.reply.it', 9998)

r.recvuntil('Password: ')
r.sendline('this_is_darth_stuff')

r.recvuntil('p: ')
p = int(r.recvuntil('\n'), 16)

r.recvuntil('Zer0 subject says: ')
pub = int(r.recvuntil('\n'), 16)

private_key = 42
public_key = pow(2, private_key, p)

r.recvuntil('What about you? ')
r.sendline(str(hex(public_key)))

shared_key = pow(pub, private_key, p)
key = int_to_bytes(shared_key)

print(key)
print(len(key))

r.recvuntil('CFB\n')

iv = base64.b64decode(r.recvuntil('\n'))
cipher = base64.b64decode(r.recvall())

print(iv)
print(cipher)

aes = AES.new(key[:16], AES.MODE_CFB, iv=iv)
print(aes.decrypt(cipher))

r.interactive()

#{FLG:fir5t_ha1f_0f_f14g_4nd_s3c0nd_ha1f_0f_f14g}
```

