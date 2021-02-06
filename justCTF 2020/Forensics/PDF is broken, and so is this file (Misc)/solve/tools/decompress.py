#!/usr/bin/env python3

import sys
import zlib

for n in sys.argv[1:]:
    with open(n, 'rb') as f:
        d = f.read()
        try:
            d = zlib.decompress(d)
        except:
            continue

        print(n)
        with open(n+'.dec', 'wb') as ff:
            ff.write(d)
