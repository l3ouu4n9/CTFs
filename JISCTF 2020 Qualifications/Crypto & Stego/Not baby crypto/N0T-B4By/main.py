import os
from os import listdir
from os.path import isfile, join
import random

data_path = 'plainData'

def encrypt(key):
    for f in listdir(data_path):
        file = join(data_path, f)
        if isfile(file):
            with open(file, 'r') as ff:
                for data in ff:
                    enc_file = join(data_path, f.split('.')[0] + '.enc')
                    with open(enc_file, 'w') as fff:
                        encrypted = list()
                        encrypted2 = list()

                        for c in data:
                            cb = int(int(bin(ord(c)), 2) ^ int(bin(key), 2))
                            encrypted.append(cb)
                        for l in encrypted:
                            cb = int(int(bin(int(l)), 2) ^ int(bin(key * 2), 2))
                            encrypted2.append(cb)
                        for l in encrypted2:
                            fff.write(str(l))

                        fff.close()
                ff.close()


def generate_key():
    ran = os.urandom(32).hex()
    key_list = list()
    n = 2
    key = int()
    [key_list.append(ran[i:i + n]) for i in range(0, len(ran), n)]
    for i in key_list:
        v = int(i, 16) % 10
        tmp = str(key) + str(v)
        key = int(tmp)
    return key

def main():
    print('Starting the encryption process..')

    x = generate_key()
    encrypt(x)


if __name__ == '__main__':
    main()
