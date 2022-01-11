from Crypto.Util.number import long_to_bytes
import gmpy2,binascii,libnum,time


def start(n, e, c):
	res = 0
	#print(time.asctime())
	for i in range(200000000):
		if gmpy2.iroot(c + n * i, 3)[1] == 1:
			res = gmpy2.iroot(c + n * i, 3)[0]
			#print(i, res)
			#print(long_to_bytes(res))
			#print(time.asctime())
			print("Successfully Cracked")
			break
	return long_to_bytes(res)