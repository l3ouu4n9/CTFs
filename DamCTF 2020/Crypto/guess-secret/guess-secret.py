#!/usr/bin/env python3

# for others
import sys
import zlib

# for crypto
import binascii
import secrets
import hashlib
from Crypto.Cipher import AES
from Crypto.Util import Counter

# make this script use unbuffered I/O
class Unbuffered(object):

      def __init__(self, stream):
           self.stream = stream

      def write(self, data):
           self.stream.write(data)
           self.stream.flush()

      def writelines(self, datas):
           self.stream.writelines(datas)
           self.stream.flush()

      def __getattr__(self, attr):
           return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)

# AES CBC ENCRYPTION object
class _AES(object):
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key).digest()
        self.counter = secrets.randbits(128)

    def encrypt(self, plaintext):
        iv = self.counter.to_bytes(16, 'little')
        counter = Counter.new(128, initial_value=int(binascii.hexlify(iv), 16))
        # create cipher
        cipher = AES.new(self.key, AES.MODE_CTR, counter=counter)
        self.counter += 1
        # return IV + encrypted_data!
        return iv + cipher.encrypt(plaintext)

    # no decryption, this is not easy!


def generate_packet(cookie, attacker_string):
    return (cookie) + attacker_string

def deflate_packet(packet):
    a = zlib.compress(bytes(packet, 'utf-8'))
    return a

def encrypt_packet(aes, packet):
    return aes.encrypt(packet)

def get_flag():
    with open('flag', 'rt') as f:
        flag = f.read()
    return flag

def heading():
    print("""Hi, we would like to introduce you a very secure and
efficient way to transfer a huge blobs of data over the Internet.
That is, compressing the data before encrypt and send out to the Internet.
We will enjoy the small size of data by applying loseless data compression,
making the communication efficient, and then applying encryption will make
the communication secure.

Does it look like we can have the cake and eat it too? We hope so.

In this 'crypto' challenge,
for a givin plaintext, what we will do is basically:

    1) compressed_data = deflate(plaintext) and
    2) encrypted_data = AES_CTR_128(compressed_data),

and we will let you do the following:

    1) You can give me a small text string. Then I will generously include
       the string in somewhere in my plaintext (check the .py code).
    2) We will compose the plaintext like the following:
        plaintext: [flag] + [your_input]
        The flag format is: dam{[0-9a-f]+} (32 hexadecimal chars in {})
    3) We will let you know about the `encrypted_data`. Although you can
       never see the plaintext directly (we believe so), I hope this helps
       you to figure out the flag in the message.

In this setup, can you steal my flag?
If you do so, you can steal my website cookie...
(inspired by BEAST / CRIME / BREACH / HEIST)...
""")


def get_string():
    string = input("please give me your string...\n")
    return string

def main():
    aes = _AES(secrets.token_bytes(16))
    flag = get_flag()
    heading()
    while True:
        attacker_string = get_string()
        packet = generate_packet(flag, attacker_string)
        deflated = deflate_packet(packet)
        encrypted = encrypt_packet(aes, deflated)
        print(encrypted)

if __name__ == '__main__':
    main()
