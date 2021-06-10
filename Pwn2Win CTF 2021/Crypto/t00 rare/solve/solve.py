from sage.all import *
from pwn import *
from ast import literal_eval
from tqdm import tqdm
from subprocess import check_output

q1 = 2 * 2 * 2 * 2 * 3 * 71 * 131 * 373 * 3407
q2 = (
    17449 * 38189 * 187019741 * 622491383 * 1002328039319 * 2624747550333869278416773953
)
q = q1 * q2 + 1
p = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
a = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC
b = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
E = EllipticCurve(Zmod(p), [a, b])
G = E(
    0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
    0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5,
)


debug_exp = None
debug_x = None


def connect(local):
    if local:
        global debug_exp, debug_x
        conn = process(["sage", "chall.sage"])
        conn.recvuntil(b"exp = ")
        debug_exp = int(conn.recvline().decode().strip())
        conn.recvuntil(b"x = ")
        debug_x = int(conn.recvline().decode().strip())
        return conn
    else:
        conn = remote("t00-rare.pwn2win.party", 1337)
        cmd = conn.recvline().decode().strip()
        token = check_output(cmd.split(" ")).decode().strip()
        conn.sendline(token)
        return conn


def get_sig(conn, h):
    conn.sendlineafter(b"4- Exit\n", "1")
    conn.sendlineafter(b"hash (hex): ", hex(h))
    conn.recvuntil(b"...\n")
    return literal_eval(conn.recvline().decode().strip())


def read_flag(conn, password):
    conn.sendlineafter(b"4- Exit\n", "3")
    conn.sendlineafter(b"password: ", str(password))


def get_target(conn):
    read_flag(conn, 0)
    conn.recvuntil(b"Signing ")
    return int(conn.recvline().decode().strip()[:-3], 16)


def bsgs_solve(r, s):
    base = power_mod(7, q2, q)
    xx = 1
    rs1 = (r * inverse_mod(s, q)) % q
    rs1G = rs1 * G
    R = E.lift_x(Integer(r))
    m = ceil(sqrt(q1))
    bound = m // 2  # requied time will be 1/2, but success probability will be 1/4
    tbl = {}
    base1 = inverse_mod(base, q)
    last = R
    for j in tqdm(range(1, bound)):
        last = last * base1
        tbl[last.xy()[0]] = j
    print("table done")
    basem = power_mod(base, m, q)
    last = rs1G
    for i in tqdm(range(0, bound)):
        xp = last.xy()[0]
        last = last * basem
        if xp in tbl:
            xxi = i * m + tbl[xp]
            print("found exponent", xxi)
            xx = power_mod(7, q2 * xxi, q)
            print("found private key", xx)
            return xx


while True:
    conn = connect(False)
    if debug_x and debug_exp:
        print("debug exp", debug_exp)
        print("debug x", debug_x)
        m = ceil(sqrt(q1))
        print("j", debug_exp % m)
        print("i", debug_exp // m)

    h = get_target(conn)
    print("target h", hex(h))
    r, s = get_sig(conn, 0)
    print("sig of 0", (r, s))
    x = bsgs_solve(r, s)
    if not x:
        print("Try next")
        continue
    print("x", x)
    r, s = get_sig(conn, h + q)
    print("sig of h", (r, s))
    k = ((h + x * r) * inverse_mod(s, q)) % q
    print("k of sig of h", k)

    print("Read flag 1")
    read_flag(conn, inverse_mod(k, q))
    conn.recvline()  # Signing...
    f1 = conn.recvline().decode().strip()
    print(f1)

    print("Read flag 2")
    read_flag(conn, -inverse_mod(k, q))
    conn.recvline()  # Signing...
    f2 = conn.recvline().decode().strip()
    print(f2)

    try:
        conn.close()
    except ex:
        print(ex)

    if "CTF-BR" in f1 or "CTF-BR" in f2:
        break
