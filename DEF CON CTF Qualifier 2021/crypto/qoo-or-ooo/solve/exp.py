from pwn import *

p = remote('qoo-or-ooo.challenges.ooo', 5000)
#p = remote('back-to-qoo.challenges.ooo', 5000)


bases = []
current_rot = 0
last_dir = 2
lose_count = 0
for i in range(30):
    p.recvuntil('Your competitor bets on ')
    comp1_bet = int(p.recvline())
    if(comp1_bet==current_rot):
        p.sendline('2')
        p.sendline('0')
    else:
        p.sendline('2')
        p.sendline(str(last_dir))
        current_rot^=1
        if(last_dir==1):last_dir = 2
        else: last_dir = 1
    p.recvuntil("zardus's competitor bets on ")
    comp2_bet = int(p.recvuntil(',')[:-1])
    my_bet = int(p.recvline().decode().split(' ')[-1])
    res = p.recvline()
    print(i, res)
    if(b"Win" in res): 
        p2_bet = my_bet^(comp1_bet*comp2_bet)
    else:
        lose_count+=1
        p2_bet = 1^my_bet^(comp1_bet*comp2_bet)
        comp2_bet = comp2_bet^1
    if(lose_count>=5):
        p.close()
        exit()
    print((comp1_bet, comp2_bet, my_bet, p2_bet))
    bases.append((comp1_bet, comp2_bet, my_bet, p2_bet))

print(bases)

print(p.recvuntil('zardus:'))

za_bases = ''
for i in range(30):
    p.recvuntil(':')
    za_bases+=str(int(p.recvline().decode().split(':')[-1]))

p.recvuntil(': -1:')
given_nonce = bytes.fromhex(p.recvline().strip().decode())
p.recvuntil(': -2:')
encrypted_flag = bytes.fromhex(p.recvline().strip().decode())


import hashlib
from Crypto.Cipher import AES
res = bases
base_p2 = list(zip(*res))[1]
bet_p2 = list(zip(*res))[3]
base = '000110010010110011110110000000'
key_array = ''
print(''.join([str(i) for i in base_p2]))
print(base)
print(bet_p2)
for i in zip(base_p2, base, bet_p2):
    if(i[0] == int(i[1])):
        key_array+=str(i[2])
print(len(key_array))

def key_array_to_key_string(key_list):
    key_string_binary = b''.join([bytes([x]) for x in key_list])
    return hashlib.md5(key_string_binary).digest()
                    
for i in range(2**(len(key_array)+1)):
    if(i%100000==0):print(i)
    secret_key = []
    for k in bin(i)[2:]:
        secret_key.append(int(k))
#    print(secret_key)
    key = key_array_to_key_string(secret_key)
#    print(key)
    cipher = AES.new(key, AES.MODE_EAX, given_nonce)
    cleartext = cipher.decrypt(encrypted_flag)

    if(b"OO{" in cleartext):
        print(i)
        print(cleartext)
        break

secret_key = []
for k in key_array:
    secret_key.append(int(k))
print(secret_key)
key = key_array_to_key_string(secret_key)
print(key)
cipher = AES.new(key, AES.MODE_EAX, given_nonce)
#cipher.nonce = given_nonce
cleartext = cipher.decrypt(encrypted_flag)

if(b"OO" in cleartext):
    pass
print(cleartext)

p.interactive()
p.close()

