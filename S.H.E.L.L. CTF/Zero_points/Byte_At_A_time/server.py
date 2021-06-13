from base64 import b64decode,b64encode
from Crypto.Cipher import AES
import os,hashlib,string,random
from flask import Flask, jsonify,request
from secret import key,flag

app = Flask(__name__)


class CookieHandler:
    def __init__(self,key):
        self.key = key

    def encrypt(self,cookieData):
        aesObj = AES.new(self.key,AES.MODE_ECB)
        ciphertext = aesObj.encrypt(CookieHandler.pad(cookieData).encode())
        return ciphertext.hex()

    def decrypt(self,encryptedCookieData):
        encryptedCookieData = bytes.fromhex(encryptedCookieData)
        aesObj = AES.new(self.key,AES.MODE_ECB)
        plaintext = aesObj.decrypt(encryptedCookieData)
        return CookieHandler.unpad(plaintext.decode())

    @staticmethod
    def pad(message):
        diff = 16 - (len(message)%16)
        return message + chr(diff)*diff

    @staticmethod
    def unpad(message):
        lastchr = ord(message[-1])
        message = message[:-lastchr]
        return message

obj = CookieHandler(key)

@app.route('/genCookie', methods=['POST'])
def genCookie():
    username = request.json["username"]
    return jsonify({'cookie': obj.encrypt(username+flag)})

if __name__ == '__main__':
    app.run(debug=False,port=8000,host="0.0.0.0")
