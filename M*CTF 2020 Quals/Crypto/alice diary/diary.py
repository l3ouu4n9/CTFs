import argparse
import random
import os

DIFFICULTY = 6

parser = argparse.ArgumentParser(description='Управление дневником')
parser.add_argument('-k', '--key', type=str, default='', help='Ключ')
parser.add_argument('file', type=str, metavar="FILE", help='Путь к записке')

args = parser.parse_args()

key = args.key
if key == '' or len(key) != DIFFICULTY:
    key = ''.join([chr(random.randint(33, 127)) for i in range(DIFFICULTY)])
    print('Новый ключ:', key)
key = list(map(ord, key))

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes(6, 'big')

def int_from_bytes(x: bytes) -> int:
    return int.from_bytes(x, 'big')

def _encode(x: int) -> int:
    return sum([key[i]*x**i for i in range(DIFFICULTY)])

def _decode(x: int) -> int:
    for i in range(128):
        if _encode(i) == x:
            return i
    return 0

if os.path.exists(args.file):
    with open(args.file, 'rb') as f:
        with open('.diary', 'wb') as o:
            while data := f.read(6):
                o.write(bytes([_decode(int_from_bytes(data))]))
                
os.system('nano .diary')

with open('.diary', 'rb') as f:
    data = f.read().strip()
    with open(args.file, 'wb') as o:
        o.write(b''.join([int_to_bytes(_encode(i)) for i in data]))
os.remove('.diary')
