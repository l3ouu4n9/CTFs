from pwn import *

ans = []
p = remote("jh2i.com", 50012)
i = 0
while True:

	p.recvuntil('>')

	if i == len(ans):
		p.sendline('0')
		p.recvuntil('W A S ')
		num = p.recvuntil('\n', drop=True)
		ans.append(str(num))
		print(ans)
		p.close()
		i = 0
		p = remote("jh2i.com", 50012)
	else:
		p.sendline(ans[i])
		i += 1