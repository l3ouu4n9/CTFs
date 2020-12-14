from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import binascii
import sys

key = b"****************"
iv = key
flag = "***********************"

def encrypt(str1):
    obj = AES.new(key, AES.MODE_CBC, iv)
    str1 = pad(str1,16)
    ciphertext = obj.encrypt(str1)
    return binascii.hexlify(ciphertext)

def decrypt(str2):
    obj=AES.new(key, AES.MODE_CBC, iv)
    plaintext=obj.decrypt(str2)
    return binascii.hexlify(plaintext)

s="""
1. Enter key and get flag
2. Encrypt plaintext
3. Decrypt ciphertext

Enter option: """

while(True):
    try:
        print(s, end='')
        opt=int(input())

        if(opt==1):
            KEY = input("Enter hex key: ")
            KEY = binascii.unhexlify(KEY)
            if(KEY==key):
                print(flag)
                break;

        elif(opt==2):
            pt = input("Enter hex plaintext: ")
            pt = pt.encode('utf-8')
            pt = binascii.unhexlify(pt)
            print("Ciphertext: ", encrypt(pt).decode('utf-8'))

        elif(opt==3):
            ct = input("Enter hex ciphertext: ")
            ct = ct.encode('utf-8')
            ct = binascii.unhexlify(ct)
            print("Plaintext: ", decrypt(ct).decode('utf-8'))

        else:
            print("The input should be in between 1 and 3")

    except:
        print("Error")