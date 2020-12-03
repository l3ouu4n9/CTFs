import hashlib
import logging

from Crypto.Cipher import AES
from flask import flash


def unpad(val):
    return val.rstrip(b'\x00')


def process(coupon, code):
    digest = coupon[-16:]
    iv = coupon[:16]
    enc = coupon[16:-16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = unpad(cipher.decrypt(enc))

    m, s, a = data.split(b"|")

    logging.debug(f"{m}, {s}, {a}")

    if digest != hashlib.md5(m+s+a).digest():
        flash("Digest invalid", "error")
        return None

    if m != magic.encode():
        flash("Magic value is malformed", "error")
        return None

    if s != str(code).encode():
        print(s)
        flash("Secret code invalid or corrupted", "error")
        return None

    return m,s,a
