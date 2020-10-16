---
layout: post
category: web
title: replyCTF 2020 - The secret Notebook
tags:
	- hrshk
---

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
