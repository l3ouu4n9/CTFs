import binascii
filename = 'm3ss4g3.msg'
with open(filename, 'rb') as f:
	content = f.read()
hexfile = binascii.hexlify(content).decode()
hexfilerev = hexfile[::-1]
binfilerev = bytes.fromhex(hexfilerev)
with open('m3ss4g3.zip', 'wb') as f:
	f.write(binfilerev)