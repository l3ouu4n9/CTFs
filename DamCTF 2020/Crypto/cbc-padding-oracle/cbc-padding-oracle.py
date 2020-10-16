#!/usr/bin/env python3

# for stdin
import sys

# for crypto
import secrets
import hashlib
from Crypto.Cipher import AES

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
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, plaintext):
        # pad data first
        padded = self._pad(plaintext)
        # get IV
        iv = secrets.token_bytes(AES.block_size)
        # create cipher
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        # return IV + encrypted_data!
        return iv + cipher.encrypt(padded)

    def decrypt(self, ciphertext):
        # get IV from the head
        iv = ciphertext[:AES.block_size]
        # create ciper
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        # decrypt and then unpad!
        return self._unpad(cipher.decrypt(ciphertext[AES.block_size:]))

    def _pad(self, c):
        # get the length
        c_len = len(c)

        # round up the length to the block size boundary
        padded_size = c_len // self.bs
        padded_size = padded_size * self.bs
        if (c_len % self.bs):
            padded_size += self.bs

        # calculate how much padding should we have
        pad_length = padded_size - len(c)

        # if this is bigger than N>0, than add N number of paddings with value N
        if (pad_length > 0):
            return (c + (bytes(chr(pad_length), 'utf-8') * pad_length))
        else:
            # else, add 16 paddings with value 16..
            return (c + (bytes(chr(16), 'utf-8') * 16))


    # ERROR here would work as padding oracle!
    # Case 1: match the padding!
    # Case 2: ERROR, padding mismatch!
    def _unpad(self, c):
        # get the last character..
        last_chr = c[-1]
        # if last character bigger than 16, bad padding! must be between 1~16
        if last_chr > 16:
            print("ERROR: Padding chr large > 16")
            return None
        # get last_chr * number...
        from_chr = bytes(chr(last_chr)*last_chr, 'utf-8')
        # get the last number bytes
        from_dec = c[-last_chr:]
        # if different, bad padding!
        if from_chr != from_dec:
            print("ERROR: padding error ")
            return None

        return c[:-last_chr]


# menu
def print_menu():
    print("PADDING ORACLE MENU")
    print("1. encrypt")
    print("2. decrypt")
    value = None
    while (type(1) != type(value)):
        try:
            buf = input("your input?\n")
            if buf == None or len(buf) == 0:
                quit()
            value = int(buf)
        except ValueError:
            return ""
        except EOFError:
            quit()

    return value


# encryption feature
def encryption(aes):
    flag = None
    try:
        with open("./flag", "rb") as f:
            flag = f.read()
    except FileNotFoundError:
        pass
    if flag == None:
        flag = b'dam{this_is_a_dummy_flag____}\n'

    print("Give me your data, I will encrypt your data like this:")
    print(" AES_CBC_256('A'*64 + [flag] + [your_data])")

    # Only allow numeric length
    length = None
    while (type(1) != type(length)):
        try:
            buf = input("Length of the input (size >= 32, multiple of 16)?\n")
            if buf == None or len(buf) == 0:
                quit()
            length = int(buf)
        except ValueError:
            pass
        except EOFError:
            quit()

    # get your input
    print("Please give me your input!")
    your_input = sys.stdin.buffer.read(length)

    # A*64 + flag + your_input will be encrypted...
    ciphertext = aes.encrypt(b'A'*64 + flag + your_input)
    print("Here's the encrypted data, length %d" % len(ciphertext))

    # you may get this as newline terminated and eval this as bytes
    print(ciphertext)


# decryption feature
def decryption(aes):
    length = None
    while (type(1) != type(length)):
        try:
            buf = input("Length of the input (size >= 32, multiple of 16)?\n")
            if buf == None or len(buf) == 0:
                quit()
            length = int(buf)
            if length < 32:
                length = None
            elif length % 16 != 0:
                length = None
        except ValueError:
            pass
        except EOFError:
            quit()
    print("Please give me your input!")
    your_input = sys.stdin.buffer.read(length)
    decrypted = aes.decrypt(your_input)
    if (decrypted == None):
        pass
    else:
        print("Your input has been successfully decrypted in length %d" % len(decrypted))

def menu(aes):
    while True:
        selection = print_menu()
        if selection == 3:
            break
        if selection == 1:
            encryption(aes)
        elif selection == 2:
            decryption(aes)
        else:
            print("No match!")
            break

def main():
    aes_key = None
    with open('aeskey', 'rb') as f:
        aes_key = f.read()
    if aes_key == None:
        print("Error no AES KEY")
        quit()

    aes = _AES(str(aes_key))
    menu(aes)

if __name__ == '__main__':
    main()
