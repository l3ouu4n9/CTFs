import base64
import itertools

x=['ODM','gxM','wNT','jgw']
perm=list(itertools.permutations(x))
for i in perm:
    flag=''.join(i)+'Mw=='
    try:
        print(base64.b64decode(flag).decode('ascii'))
    except:
        continue