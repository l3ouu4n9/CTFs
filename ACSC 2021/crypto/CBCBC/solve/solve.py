#!/usr/bin/env python3

from pwn import process, remote
from base64 import b64decode, b64encode

# io = process(["python", "chal.py"])
io = remote("cbcbc.chal.acsc.asia", 52171)
io.sendlineafter(b"> ", b"1")
io.sendlineafter(b"username: ", b"")
io.recvuntil(b"token: \n")
enc = b64decode(io.recvline().strip())
iv1, iv2, ct = enc[:16], enc[16:32], enc[32:]


def oracle(iv, block):
    enc = iv + iv2 + block
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b"username: ", b"l3o")
    io.sendlineafter(b"token: ", b64encode(enc))
    r = io.recvlineS()
    return "Check your token again" not in r


def oracle2(iv, block):
    enc = iv1 + iv + block
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b"username: ", b"l3o")
    io.sendlineafter(b"token: ", b64encode(enc))
    r = io.recvlineS()
    return "Check your token again" not in r


# copied from https://gist.github.com/maple3142/e9f41bc7dba159123d9c7546e406948b


def cbc_oracle_block(oracle, prev, block, sz=16):
    rprev = prev[::-1]
    rpt = bytearray(sz)  # reversed plaintext
    for i in range(sz):
        pad = i + 1
        for b in range(256):
            riv = bytearray(rpt)
            for j in range(i):
                riv[j] = rpt[j] ^ rprev[j] ^ pad
            riv[i] = b
            if oracle(riv[::-1], block):
                rpt[i] = pad ^ rprev[i] ^ b
                break
        print(i, bytes(rpt[::-1]))
    return bytes(rpt[::-1])


def cbc_oracle(oracle, iv, ct, sz=16):
    blocks = [iv] + [ct[i : i + sz] for i in range(0, len(ct), sz)]
    pt = b""
    for block, prev in zip(blocks[::-1], blocks[:-1][::-1]):
        pt = cbc_oracle_block(oracle, prev, block) + pt
    return pt


print(len(ct))  # 48, 3 blocks
print(cbc_oracle_block(oracle, iv1, ct[:16]))  # block 1
# b'{"username": "R3'
print(cbc_oracle_block(oracle2, iv2, ct[:32]))  # block 2
# b'dB1ackTreE", "is'
print(cbc_oracle_block(oracle2, ct[:16], ct[16:]))  # block 3, useless

# Create User
# Enter Empty name
# Token: s5Mp9+fERnm5de8qu4AYVlYAFbGORnCFQ7Q7SN/0Heoh6NbG8oiJQ+HAjq/m9Mt8rYr17D7a7LK+gi4fhr4jMa0PfahRAGbUC+XkPNrgnag=
# Login
# Username: R3dB1ackTreE
# Token: s5Mp9+fERnm5de8qu4AYVlYAFbGORnCFQ7Q7SN/0Heoh6NbG8oiJQ+HAjq/m9Mt8rYr17D7a7LK+gi4fhr4jMa0PfahRAGbUC+XkPNrgnag=
# Show Flag
# ACSC{wow_double_CBC_mode_cannot_stop_you_from_doing_padding_oracle_attack_nice_job}