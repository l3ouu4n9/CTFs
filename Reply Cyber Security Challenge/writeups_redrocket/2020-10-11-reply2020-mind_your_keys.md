---
layout: post
category: crypto
title: replyCTF 2020 - mind your keys
tags: 
    - rixxc
---

# Overview

The task provides 20000 RSA public keys and encrypted messages.

# Exploit

At first we thought about Hastad's Broadcast Attack. But the used e is 65537 and therfor we don't have enough messages to use this attack.

After some time we had the idea to check the keys for shared prime factors which turned out to be the right direction.

We used the following script to find the shared factors:

```python
import OpenSSL.crypto as crypto
from Crypto.Util.number import inverse
from functools import reduce
import operator
from decimal import Decimal
import traceback
import base64
import math
import sys
import multiprocessing
import os

def chunk(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


n = []

for i in range(1,20000):
    with open(f'keys/key{i}.pem') as f:
        n.append(int(crypto.load_publickey(crypto.FILETYPE_PEM,f.read()).to_cryptography_key().public_numbers().n))


def run(r):
    for i in r:
        for j in range(i+1,20000-1):
            #print(i,j)
            if math.gcd(n[i], n[j]) != 1:
                print(i,j, n[i], n[j])

for r in chunk(range(1,20000-1), os.cpu_count()):
    multiprocessing.Process(target=run, args=(r,)).start()
```

With one of the prime factors we could calculate the other prime factor and recover the private key. This could be used to decrypt the corresponding message.

To decrypt the message RsaCtfTool was used:

```bash
base64 -d msgs/msgs19440.enc >19440

RsaCtfTool -n 885298393006033668751086318885146695676836762845313136887911238431382126819742400577090575256175683441061279892917722883645095076312924435907172034056837944859115416066206858043320018002015284338394106544079988672699067582843214186140046282170399332979288752018228628021583847128151557558317061222308522448349488886444220896137183015667519699881758344832563326665681330532975990870313089468727707476519203257237950353594041238660408135407269163142435004513638611 -p 1015155878909680562221398235963073566637283630099630019001448387633204489019244877796744804401559234413826094271477574054262756393007301763304045778966571605511981582575171708926364520591552379670494655116847883518581699106610444663 -q 872081235402863244049578501770041611646671995644878394382691700217377175234824969709499912062769454439030355853011629933842247343577949021299083155790072318941461324336543477247388186731903752786798075478951541203518116108541080197 -e 65537 --uncipherfile 19440
```