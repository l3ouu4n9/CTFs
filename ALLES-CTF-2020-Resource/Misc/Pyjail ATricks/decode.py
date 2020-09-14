from pwn import *

enc = 'p\x7f\x7frbH\x00DR\x07CRUlJ\x07DlRe\x02N'
print xor(enc, 'ALLES{') # 1337
print xor(enc, '1337')