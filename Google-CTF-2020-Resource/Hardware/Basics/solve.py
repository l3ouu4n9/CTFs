kittens = "{:b}".format(3008192072309708).rjust(56,'0')

magic =  kittens[42:56] + kittens[10:30] + kittens[30:42] + kittens[0:10]

l = []
for i in range(0, 56, 7):
	l.append(magic[i:i+7])

m = [0, 0, 0, 0, 0, 0, 0, 0]
m[0] = l[0]
m[1] = l[7]
m[2] = l[3]
m[3] = l[5]
m[4] = l[4]
m[5] = l[1]
m[6] = l[2]
m[7] = l[6]


order = [0, 5, 2, 7, 4, 1, 6, 3]
l = []
for i in order:
	l.append(chr(int(m[i], 2)))

print('Password: ' + ''.join(l))