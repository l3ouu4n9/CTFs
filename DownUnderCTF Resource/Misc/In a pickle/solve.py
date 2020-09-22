import pickle
import string

f = open('./data', 'r')
d = pickle.load(f)
f.close()

flag = ''
for i in range(1, len(d)):
	if type(d[i]) == int:
		flag += chr(d[i])
	else:
		flag += d[i]

print(flag)