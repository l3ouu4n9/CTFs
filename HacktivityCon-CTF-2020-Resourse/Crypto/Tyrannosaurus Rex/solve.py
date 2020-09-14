import base64
import binascii

c = b'37151032694744553d12220a0f584315517477520e2b3c226b5b1e150f5549120e5540230202360f0d20220a376c0067'

def dec(c):
	z = list(binascii.unhexlify(c))
	e = 'Z'
	first = 90
	i = 0
	while i < len(z):
		first ^= z[i]
		e += chr(first)
		i += 1
	f = base64.b64decode(e)
	print(f)

dec(c)