---
layout: post
category: misc
title: replyCTF 2020 - Signals from the past
tags:
    - LevitatingLion
---

For this challenge we are provided with a capture file from a logic analyzer, in the format supported by `sigrok`. This can be parsed using `sigrok` or the GUI frontend `pulseview`.

The capture has a total of 8 probes, but only two of them show interesting signals. I tried various decoders, to find out that this was a UART communication. It looks like a keyboard talking to a normal linux system: the user logs in using username and password and is dropped into a shell. `ls` shows the files `cmds encoder secret_msg.txt send_bin`, then `./send_bin encoder` is run.

After that follows a long stream of binary data, what appears to be a slightly encoded ELF file. Dumping the data into a file confirms that suspicion: there's a leading `0xC0` byte which doesn't belong into the ELF magic, an intact ELF header follows. However, due to the encoding the section headers appear corrupted and we cannot properly analyze the binary.

I have no idea about what encodings are normally used in this UART context; searching the web quickly turned to Consistent Overhead Byte Stuffing, but that doesn't fit the data we have at all. After an hour of senseless googling, I finally stumbled upon [this code](https://android.googlesource.com/kernel/msm/+/android-7.1.0_r0.2/drivers/bluetooth/hci_bcsp.c#133) in android's bluetooth stack. Apparently, this encoding is part of BCSP, used when talking UART over Bluetooth. The encoding is simple: take your data, escape every `DB` byte by replacing it with `DB DD`, escape every `CO` byte by replacing it with `DB DC`, then prepend and append a `CO` byte.

Decoder script:

```py
from pwn import *

dump = read("elf_dump")
dump = dump[1:-1]

idx = 0
out = b""
while True:

    x = dump[idx]
    if x == 0xdb:
        y = dump[idx+1]
        if y == 0xdc:
            x = 0xc0
        elif y == 0xdd:
            x = 0xdb
        else:
            assert False
        idx += 1
    out += bytes([x])

    idx += 1
    if idx >= len(dump):
        break

write("out.elf", out)
```

After decoding the binary, we obtain a completely valid ELF file, and can analyze it as usual: the binary takes two file names as command line arguments. It reads the contents of the second file, XORs them with the constant string `dqjg0843jgnjern738ewp2`, and appends the result to the second file.

Searching the files we have for anything with stray data appended, we notice `logic-1-4` in the capture file (which is actually a zip file) ends with a bunch of random looking bytes (we can also see these bytes at the end of the displayed capture, where all signals jump erratically). XORing them with the fixed string from above result in the flag.

Flag: `{FLG:s3r14l_bd_m4st3r}`
