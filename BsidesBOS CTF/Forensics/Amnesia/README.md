# Amnesia
Ohh no! I can't remember anything, where have I been? 

## Writeup
1. We are given a file `image.bin`.
2. Get the image info with `python vol.py -f image.bin imageinfo`
3. Take a look at its chrome history `python vol.py -f image.bin --profile=Win7SP1x86_23418 chromehistory`, the flag shows.
```
https://bsidesbos.ctf.games/?flag=flag%7Bforensic_cookie_hunter%7D
```