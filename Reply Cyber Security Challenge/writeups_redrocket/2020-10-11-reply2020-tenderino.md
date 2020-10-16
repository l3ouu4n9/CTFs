---
layout: post
category: rev
title: replyCTF 2020 - tender.ino
tags: 
    - kowu
---

## Overview

We get a `tender.ino.hex` file. From the filename I assumed an arduino `hex` image. To reverse it, I need it in `bin` format, so I first converted it:
```
objcopy -I ihex tender.ino.hex -O binary tender.bin
```
Simulating it in simavr (atmgea328p because this is the basic arduino MCU, and 16MHz) gives us the following output:
```
user@KARCH ~/ctf/reply % simavr -m atmega328p -f 16000000 tender.ino.hex
Loaded 1 section of ihex
Load HEX flash 00000000, 4308
         .....           ......
   ,ad8PPPP88b,     ,d88PPPP8ba,.
  d8P"      "Y8b, ,d8P"      "Y8b.
 dP'           "8a8"           `Yd.
 8(              "              )8.
 I8                             8I.
  Yb,                         ,dP.
   "8a,                     ,a8".
     "8a,                 ,a8".
       "Yba             adP"     The game of love <3 .
         `Y8a         a8P'.
           `88,     ,88'          Unlock the love!! .
             "8b   d8".
              "8b d8".
               `888'.
                 ".
..
..
.

```
However, using this kind of emulation it does NOT forward stdin input to UART0, neither do timers seem to work, as I found out.
So I compiled simavr on my own, and in the `simavr/examples/board_simduino/` a (more) proper emulator can be found (after build)) as `simduino.elf`. Before compilation, set `export SIMAVR_UART_XTERM=1`.
Next try. Launch simduino with the `-d` option for a gdb debugging server:
```
user@KARCH ..board_simduino/obj-x86_64-pc-linux-gnu (git)-[master] % ./simduino.elf -d ~/ctf/reply/tender_fake.ino.hex
atmega328p booloader 0x00000: 4308 bytes
avr_special_init
avr_gdb_init listening on port 1234
uart_pty_init bridge on port *** /dev/pts/1 ***
uart_pty_connect: /tmp/simavr-uart0 now points to /dev/pts/1
note: export SIMAVR_UART_XTERM=1 and install picocom to get a terminal
gdb_network_handler connection opened
```
Attach a terminal to UART0:
```
user@KARCH ~ % picocom /tmp/simavr-uart0 --omap crlf              
picocom v3.1

port is        : /tmp/simavr-uart0
flowcontrol    : none
baudrate is    : 9600
parity is      : none
databits are   : 8
...
```
Attach radare (set bpinmaps=false to get breakpoints working), and continue execution with the `dc` command:
```
user@KARCH ~ % r2 -a avr -e dbg.bpinmaps=false -D gdb gdb://localhost:1234
WARNING: r_file_exists: assertion '!R_STR_ISEMPTY (str)' failed (line 164)
gdbr_get_reg_profile: unsupported x86 bits: 8
cannot find gdb reg_profile
= attach 0 0
 -- Buy a Mac
[0x00000000]> dc
```
Now we can see that on the UART additionally the following is printed: `Welcome to the game of love, enter the key of my heart:`. Character by character, with a small delay in between.
Also UART input works (I confirmed that the ISR got hit), HOWEVER some parts of the Simulation are still non-functioning. I don't know exactly which, but the Program just did not react on input at all. Might be timer related. But this couldn't stop me from reversing. However it took a huge amount of time trying to (unsuccessfully) get it to react on input...

## Reversing / Debugging

For reversing I used Ghidra. First of all I tried to locate the mainloop. I did this by trying to find out where the `Welcome to the...` string comes from, as it is not visible in plaintext inside the binary. By halting execution during printing of the message, and stepping out of the funtions, I found at `0x283` something what looked like a decryption routine. Basically it xors something with 0x24.
```c
char * decrypt_string(char *param_1)
{
  undefined2 uVar1;
  int iVar2;
  byte *pbVar3;
  
  iVar2 = R23R22;
  uVar1 = R17R16;
  R17R16 = param_1;
  param_1 = malloc(R23R22);
  Z = R17R16;
  X = param_1;
  Y._0_1_ = (byte)iVar2;
  Y._1_1_ = (char)((uint)iVar2 >> 8) + W._1_1_ + CARRY1((byte)Y,(byte)W);
  R19 = 0x24;
  Y._0_1_ = (byte)Y + (byte)W;
  do {
    pbVar3 = X;
    R18 = *Z;
    Z = Z + 2;
    R18 = R18 ^ R19;
    X = X + 1;
    *pbVar3 = R18;
  } while ((byte)X != (byte)Y || X._1_1_ != (char)(Y._1_1_ + ((byte)X < (byte)Y)));
  R17R16 = (byte *)uVar1;
  return (char *)param_1;
}
```
Note: Relying on the ghidra generated C code is somethimes not the best, as one can see it is very verbose for the AVR architecture. Most of the time just looking at assembly is better in my optinion.

Now dumping encrypted memory regions end decrypting them is easy (I used r2 with `pcp`).
```python
import struct
buf = struct.pack ("336B", *[
0x70,0x00,0x4c,0x00,0x4d,0x00,0x57,0x00,0x04,0x00,0x4d,
...
0x50,0x00,0x1e,0x00,0x04,0x00])

print(''.join([chr(b ^ 0x24) for b in buf if b]))
```
We get the following:
```
This is not the right key... do you really love me??O Romeo, Romeo, wherefore art thou Romeo? Take all myself!!
Welcome to the game of love, enter the key of my heart: 
```
Interesingly, there seems to be a failure message `This is not the right key...` and a success message `O Romeo, Romeo, ...`. By following xrefs of the decryption routine, I found the origin where it is called (`0x4e3` in ghidra):
```c
    if (wrongkey) {
      param_1 = (char *)0x34;
                    /* This is not the right key */
      W = (byte *)0x100;
    }
    else {
      param_1 = (char *)0x3b;
                    /* Romeo Romeo */
      W = (byte *)0x168;
    }
    W = (byte *)decrypt_string(W,param_1);
    print_string((char *)W);
```
Right above, there is a loop checking some computed values against a static key (`0xe77` in radare). So next up I placed a breakpoint on the comparison an waited for it to trigger. Which never happened, because of unknown reasons...
It would always end up waiting for some bits of a singly byte in memory to be set, which never happened. In the same piece of code responsible for this, there was also a lot of timer related stuff involved. I guess depending on the input (length?) LEDs are PWM driven to pulsate faster or something like that.
I got really annoyed that I could not find out what is setting those bits, so I just manually overwrote the location with 0xff. Now all bits are set and my breakpoint triggered. Nice. But we are probably working on an unintended program state (which turned out doesn't matter that much).

I wanted to know where the Values we compared against originated from. So I got interested in the loop right above the key comparison. Apparently this loop was responsible for converting a potential input char by char to compare it with the static key!
```c
do {
    R21R20._0_1_ = *param_4; // read in a single char (placed breakpoint here)
    X = param_4 + 1;
    param_4 = X;
    R0 = (byte)R21R20 * '\x02';
    if (((byte)R21R20 & 1) == 0) { // is uneven?
    W._0_1_ = (byte)R21R20 + (byte)Z;
    param_2 = CONCAT11(((Z._1_1_ - CARRY1((byte)R21R20,(byte)R21R20)) +
                        CARRY1((byte)R21R20,(byte)Z)) * '\x02' + CARRY1((byte)W,(byte)W),
                        (byte)W * '\x02');
    W._0_1_ = (byte)W * '\x06';
    param_1 = (char *)R7R6;
    }
    else {
    W._0_1_ = (byte)R21R20 + 3;
    param_2 = CONCAT11((char)(param_2 >> 8),3);
    do {
        W._0_1_ = (byte)W * '\x02';
        R21R20._0_1_ = (byte)R21R20 - 1;
        param_2 = param_2 & 0xff00 | (uint)(byte)R21R20;
    } while ((byte)R21R20 != 0);
    param_1 = (char *)R5R4;
    }
    W = (byte *)idkwhatthisdoes((byte)W);
    Y[1] = W._1_1_; // write bytes (step until here)
    *Y = (byte)W;
    Z = (byte *)((int)Z + 1);
    Y = Y + 2;
} while ((byte)Z != 0x20 || Z._1_1_ != (byte)(R1 + ((byte)Z < 0x20)));
```
So I placed a breakpoint at `0x4b4` (it is a `ld R20, X+` instruction), and faked my way through until I hit the breakpoint. Then I inspected the memory at X `s r27 * 0x100 + r26 + 0x800000`. X is a R27:R26 composite register, and RAM is located at 0x800000 in qemu. I overwrote the content at this address with the known prefix of the flag (`pz {FLG:AAAA`). After I stepped until where the resulting byte is written, it was equal to the first entry of the static key! So now I saved the static key (`pcp`) and tried to recreate the functionality in Python.

It was way easier to do this just by looking at the assembly. As AVR has no multiplication instructions (I guess) the Compiler generated some funny code. E.g. multiplying by 8 is equal to shifting left 3 times in a loop.
```python
# c is character, i is index
def crypt(c, i):
    res = ord(c)
    if res & 1:
        res += 3
        res *= 8
    else:
        res += i
        res *= 6
    # idkwhatthisdoes()
    return res
```
This already lead to the correct key generation for most of the input chars (e.g. `{` was not correct). However there was still the `idkwhatthisdoes` function in between. I don't know what it really does.
But by debugging and via try and error I found out, that as a good guess it would subtract ~700 (always a multiple of 100, maybe some modulo 100 stuff?) if the value was above ~700. Good enough for me :)

So I manually found out every new char, and whenever my `idkwhatthisdoes` function estimation was wrong (which was rarely the case), I would simply add an exception to the crypt function, as it was easy to spot the correct value (if the last two digits matched, and the resulting sentence made sense).
```
import struct
import string

buf = struct.pack("64B", *[
    0x34, 0x01, 0xaa, 0x01, 0xd4, 0x01, 0x50, 0x02, 0x74, 0x01, 0xb4,
    0x00, 0x84, 0x00, 0x24, 0x01, 0x54, 0x00, 0x9a, 0x02, 0xd4, 0x00,
    0xee, 0x02, 0x54, 0x00, 0x06, 0x03, 0xc4, 0x02, 0x84, 0x00, 0x54,
    0x00, 0xf2, 0x01, 0xd4, 0x00, 0xd4, 0x00, 0xb4, 0x00, 0x54, 0x00,
    0xd4, 0x00, 0xee, 0x02, 0x54, 0x00, 0x1e, 0x03, 0xd4, 0x00, 0xc2,
    0x01, 0x4c, 0x00, 0x84, 0x00, 0x20, 0x01, 0x44, 0x01])

buf2 = []

for i in range(0, len(buf), 2):
    val = buf[i] | (buf[i + 1] << 8)
    buf2.append(val)


def crypt(c, i):
    res = ord(c)
    if res & 1:
        res += 3
        res *= 8
    else:
        res += i
        res *= 6

    if res == 798:
        return res

    if res > 778:
        res -= 700

    if res == 176:
        res -= 100

    return res


# {FLG:key_for_the_Book_of_lo0ve!}
guess = '{FLG:key_for_the_Book_o'
for g in string.printable:
    e = []
    for i, c in enumerate(guess + g):
        e.append(crypt(c, i))
    if e == buf2[:len(e)]:
        print(guess + g)
        break
```

## Various Notes

* In ghidra / and during debugging with r2/gdb addresses are different. Apparently there is a PC and a PC2 in avr. To get a debugging address, just multiply the ghidra address by 2. The other way round just divide by 2.

* There is a delay function at `0x230` which makes emulated debugging awfully slow. I guess it is a delay function because some calculation with 1000 (0x3e8) takes place and data modified by the timer ISR is accessed. I placed a ret right at the beginning to make it a no op. (open in radare with `-w` switch, then `wa ret` at the desired instructions)


# The secret Notebook
## Overview
The task is a rot47 encoder/decoder. Since it is symetric, encoding and decoding are the same operations. So encode(encode("string")) == "string".
I looked at the headers but it wasn't hinting that the server is using python in its backend. Eventually I guessed it.
As the output of the challenge contained the decoded string, I tried SSTI (Server Side Template Injection). Encoding our payload and passing it to the encoder again, when it's going to output the encoded string, it will interpret is as a part of the template and execute it. I tried `{{2*2}}` as my first payload, encoded it with ROT47, then encoded it again and I got the result 4. :)

`{{}}` looks like a jinja2 template. So I went on with trying some jinja2 payloads. I tried doing `{{config}}` and it returned the configuration file and also a fake flag in the SECRET_KEY value. (troll).

We need RCE. So I tried the following payload later.
`{{config.__class__.__init__.__globals__['os'].popen('ls').read()}}`.
However `.` seemed to be blacklisted / escaped (like a lot of other stuff as well). Maybe even only a whitelist in place.
I guessed that there could be a regex in the backend responsible for filtering. So why don't we try to bypass it with a newline character.

Final payload:
```
\n (we need to escape it when encoding it.)
{{config.__class__.__init__.__globals__['os'].popen('ls').read()}}
```
Encode it, encode the encoded string (to decode it), jinja2 renders the injected template.
```
\n
(encoded payload)
```
And guess what we have RCE.
```
In case modifier /m is not (globally) specified, regexp should avoid using dot . symbol, which means every symbol except newline (\n). It is possible to bypass regex using newline injection.
```
There is a file called flag.txt. `cat flag/flag.txt` for the flag. :)

