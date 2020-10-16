---
layout: post
category: misc
title: replyCTF 2020 - Forenseec
tags:
    - LevitatingLion
---

For this challenge we are provided with the memory dump of a Windows 10 VM. The go-to tool to analyze this is, of course, volatility. The latest release of volatility doesn't have a profile for the specific Windows version, but the latest version from git works fine.

Using `pslist` we can see two interesting processes running: `TimeVault.exe` and `firefox.exe`.

# TimeVault

`TimeVault.exe` appears to be a custom binary, so we dump it into a file to analyze it. It's a .NET executable, so we can easily reverse it using dnSpy: the binary asks for a password and decrypts a hardcoded encrypted flag using this password.

As we already noticed the Firefox process earlier, this is probably were we can find the password.

# Firefox

Firefox actually runs multiple times, one main process, one GPU process and one process per open tab. For analisis, I just dumped the memory from all processes and mashed it together into one big file.

Grepping the memory for `timevault`, we can see that the URL `http://timevault.ddns.net:8080/`. The websites content are also contained in memory:

```
<html>
    <head>
        <style>
body {
  background-image: url('/static/background.jpg');
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: cover;
}</style>

<title>Home - TimeVault Website</title>
    </head>
    <body>
    </body>
<!--if my calculations are correct, when this challenge hits 88 miles per hour, you're gonna see some serious PWD c54a1db0b68d3c039df1e25569fc67b7-->
</html>
```

So the password to the TimeVault is `c54a1db0b68d3c039df1e25569fc67b7`. Giving this password to `TimeVault.exe` (which is still runnable, despite being dumped from memory) reveals ~~the flag~~ a random URL: `gamebox1.reply.it/b8216e21b7d4030dc263f82416389175/Wait_a_minute_Zer0_Are_you_telling_me_you_built_a_time_challenge_out_of_a_DeLorean`

## Flag

The above URL is only accessible after passing HTTP Basic auth, so we somehow have to obtain the username and password. The username is probably `Zer0` or `zer0` because it's their TimeVault, but how do we get the password?

Maybe Zer0 used the same password for the TimeVault and the Windows account. Using `hashdump` we can obtain the hash of the user account: `Zer0:1001:2353805c3d4da9b7c6fe8d78f7ef5e96:ea3131a50e74b42badf54b672fc7a48d:::`. All my cracking attempts were unsuccessful, but then I stumbled upon the output of `lsadump`:

```
L$_SQSA_S-1-5-21-2222777348-539284984-4271348667-1001
0x00000000  06 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x00000010  7b 00 22 00 76 00 65 00 72 00 73 00 69 00 6f 00   {.".v.e.r.s.i.o.
0x00000020  6e 00 22 00 3a 00 31 00 2c 00 22 00 71 00 75 00   n.".:.1.,.".q.u.
0x00000030  65 00 73 00 74 00 69 00 6f 00 6e 00 73 00 22 00   e.s.t.i.o.n.s.".
0x00000040  3a 00 5b 00 7b 00 22 00 71 00 75 00 65 00 73 00   :.[.{.".q.u.e.s.
0x00000050  74 00 69 00 6f 00 6e 00 22 00 3a 00 22 00 57 00   t.i.o.n.".:.".W.
0x00000060  68 00 61 00 74 00 20 00 77 00 61 00 73 00 20 00   h.a.t...w.a.s...
0x00000070  79 00 6f 00 75 00 72 00 20 00 66 00 69 00 72 00   y.o.u.r...f.i.r.
0x00000080  73 00 74 00 20 00 70 00 65 00 74 00 19 20 73 00   s.t...p.e.t...s.
0x00000090  20 00 6e 00 61 00 6d 00 65 00 3f 00 22 00 2c 00   ..n.a.m.e.?.".,.
0x000000a0  22 00 61 00 6e 00 73 00 77 00 65 00 72 00 22 00   ".a.n.s.w.e.r.".
0x000000b0  3a 00 22 00 62 00 65 00 64 00 74 00 69 00 6d 00   :.".b.e.d.t.i.m.
0x000000c0  65 00 62 00 75 00 64 00 64 00 79 00 22 00 7d 00   e.b.u.d.d.y.".}.
0x000000d0  2c 00 7b 00 22 00 71 00 75 00 65 00 73 00 74 00   ,.{.".q.u.e.s.t.
0x000000e0  69 00 6f 00 6e 00 22 00 3a 00 22 00 57 00 68 00   i.o.n.".:.".W.h.
0x000000f0  61 00 74 00 19 20 73 00 20 00 74 00 68 00 65 00   a.t...s...t.h.e.
0x00000100  20 00 6e 00 61 00 6d 00 65 00 20 00 6f 00 66 00   ..n.a.m.e...o.f.
0x00000110  20 00 74 00 68 00 65 00 20 00 63 00 69 00 74 00   ..t.h.e...c.i.t.
0x00000120  79 00 20 00 77 00 68 00 65 00 72 00 65 00 20 00   y...w.h.e.r.e...
0x00000130  79 00 6f 00 75 00 20 00 77 00 65 00 72 00 65 00   y.o.u...w.e.r.e.
0x00000140  20 00 62 00 6f 00 72 00 6e 00 3f 00 22 00 2c 00   ..b.o.r.n.?.".,.
0x00000150  22 00 61 00 6e 00 73 00 77 00 65 00 72 00 22 00   ".a.n.s.w.e.r.".
0x00000160  3a 00 22 00 62 00 65 00 64 00 74 00 69 00 6d 00   :.".b.e.d.t.i.m.
0x00000170  65 00 62 00 75 00 64 00 64 00 79 00 22 00 7d 00   e.b.u.d.d.y.".}.
0x00000180  2c 00 7b 00 22 00 71 00 75 00 65 00 73 00 74 00   ,.{.".q.u.e.s.t.
0x00000190  69 00 6f 00 6e 00 22 00 3a 00 22 00 57 00 68 00   i.o.n.".:.".W.h.
0x000001a0  61 00 74 00 20 00 77 00 61 00 73 00 20 00 79 00   a.t...w.a.s...y.
0x000001b0  6f 00 75 00 72 00 20 00 63 00 68 00 69 00 6c 00   o.u.r...c.h.i.l.
0x000001c0  64 00 68 00 6f 00 6f 00 64 00 20 00 6e 00 69 00   d.h.o.o.d...n.i.
0x000001d0  63 00 6b 00 6e 00 61 00 6d 00 65 00 3f 00 22 00   c.k.n.a.m.e.?.".
0x000001e0  2c 00 22 00 61 00 6e 00 73 00 77 00 65 00 72 00   ,.".a.n.s.w.e.r.
0x000001f0  22 00 3a 00 22 00 62 00 65 00 64 00 74 00 69 00   ".:.".b.e.d.t.i.
0x00000200  6d 00 65 00 62 00 75 00 64 00 64 00 79 00 22 00   m.e.b.u.d.d.y.".
0x00000210  7d 00 5d 00 7d 00 00 00 00 00 00 00 00 00 00 00   }.].}...........
```

This seems to contain some "security questions" and their answers. Zer0 always answered `bedtimebuddy`, and sure enough, that's the password for the Basic auth!

Flag: `{FLG:3v3n_R4M_l4st_f0r3v3r}`
