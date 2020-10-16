---
layout: post
category: coding
title: replyCTF 2020 - Wells-read
tags:
    - LevitatingLion
---

For this challenge we were provided with a version of "The Time Machine" by H. G. Wells where some of the words were slightly mangled, with individual characters replaced.

I found an original version of the novel [online](https://www.gutenberg.org/ebooks/35). As this version matches the one of the challenge closely, I think this is also the version the challenge author used. After converting the fancy unicode quotes and dashes to ASCII, we can diff the two files to obtain all mangled words:

```sh
git diff --no-index --word-diff=porcelain \
        hgwells_orig.txt 'The Time Machine by H. G. Wells.txt' \
    | grep -E '^[+-]' \
    > diff
```

We obtain the flag by concatenating all replaced characters in the mangled words:

```py
def doit(orig, new):
    global sol
    if len(orig) != len(new):
        return

    for a, b in zip(orig, new):
        if a != b:
            sol += b


sol = ""
for l in open("x"):
    x = l.strip()[1:]
    if l[0] == "-":
        orig = x
    else:
        new = x
        doit(orig, new)
print(sol)
```

Flag: `{FLG:1_kn0w_3v3ryth1ng_4b0ut_t1m3_tr4v3ls}`
