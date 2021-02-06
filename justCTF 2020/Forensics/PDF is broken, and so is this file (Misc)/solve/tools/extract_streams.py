#!/usr/bin/env python3

with open('challenge.pdf', 'rb') as f:
    data = f.read()

cnt = 0
while b'stream' in data:
    start = data.index(b'stream')
    print(start, len(data))

    end = data.find(b'endstream', start)
    print('find:', start, end)

    sub = data[start+len(b'stream')+1:end-1]
    with open(f'{cnt}', 'wb') as f:
        f.write(sub)
    print(len(sub))
    data = data[end+len(b'endstream'):]
    cnt += 1
