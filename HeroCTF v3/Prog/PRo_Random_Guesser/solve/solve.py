import re
from pwn import remote
from randcrack import RandCrack

io = remote('chall0.heroctf.fr', 7003)
io.recvuntil('Guess me')

rc = RandCrack()

for i in range(624):
    print(i)
    io.send(str(i) + '\n')
    rtn = io.recvline().decode()
    rc.submit(int(re.findall(r"was (\d+) :", rtn)[0]))
    io.recvuntil('Guess me')
num = rc.predict_randrange(0, 4294967295)
print("Cracker result: {}".format(num))
io.sendline(str(num))
io.interactive()
# how can you be so lucky... here you go... Hero{n0t_s0_r4nd0m_4ft3r_4ll}