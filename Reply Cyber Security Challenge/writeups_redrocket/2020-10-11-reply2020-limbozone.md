---
layout: post
category: coding
title: replyCTF 2020 - LimboZone -?-> LimboZ0ne
tags:
    - LevitatingLion
---

For this challenge we were provided with a `level_0` 7z archive containing two images and an encrypted `level_1` 7z archive. It also contained a python script hinting that the password for the encrypted archive is of the form `x|y|r1|g1|b1|r2|g2|b2`, where `x` and `y` are pixel coordinates and `r1`, `g1`, `b1`, `r2`, `g2`, `b2` are the pixel values of the two images at these coordinates. The two images were very similar, different only in exactly one pixel. So of course this was the pixel forming the encryption password.

Inside the archive for level 1, we find the exact same setup: two images and an encrypted 7z archive for level 2. Using a script we can easily automate this process, to unpack all levels until the last archive hopefully contains the flag.

After unpacking the first few levels, the one of the images is flipped relative to the other, so we quickly consider that in our script: when the images differ in more than one pixel, we flip one image and try again.

As we race through the levels, we encounter more such transformations: one image is flipped along one or both axes, or along the rising diagonal (which effectively swaps x and y coordinates). We can counter these in the same fashion, applying the transformations in order until the images differ in only one pixel.

All of that is automated by this top CTF-quality script:

```py
import os
import imageio

def get_pw(im1, im2, flip, flip2, swap):
    r=None
    for y in range(len(im1)):
        for x in range(len(im1[y])):
            p1 = im1[y][x]
            a = len(im1) - 1 - y if flip else y
            b = len(im1[y]) - 1 - x if flip2 else x
            if swap:
                p2 = im2[b][a]
            else:
                p2 = im2[a][b]

            if (p1 != p2).any():
                r1, g1, b1 = p1
                r2, g2, b2 = p2
                rgb1 = '{:0{}X}'.format(r1, 2) + '{:0{}X}'.format(g1, 2) + '{:0{}X}'.format(b1, 2)
                rgb2 = '{:0{}X}'.format(r2, 2) + '{:0{}X}'.format(g2, 2) + '{:0{}X}'.format(b2, 2)
                if r is not None:
                    print("fail")
                    return None
                r= str(x)+str(y)+rgb1+rgb2
                print(r)
    return r

level = 0
while True:
    im1 = imageio.imread("level_%d.png" % level)
    im2 = imageio.imread("lev3l_%d.png" % level)

    pw = None

    if im1.shape == im2.shape:
        if pw is None:
            pw = get_pw(im1,im2,False,False,False)
        if pw is None:
            pw = get_pw(im1,im2,True,False,False)
        if pw is None:
            pw = get_pw(im1,im2,False,True,False)
        if pw is None:
            pw = get_pw(im1,im2,True,True,False)
    if pw is None:
        pw = get_pw(im1,im2,False,False,True)
    if pw is None:
        pw = get_pw(im1,im2,True,False,True)
    if pw is None:
        pw = get_pw(im1,im2,False,True,True)
    if pw is None:
        pw = get_pw(im1,im2,True,True,True)

    if pw is None:
        print("FAIL")
        break
    print(level, pw)
    level += 1
    os.system("7z e -p'%s' level_%d.7z && rm -f level_%d.7z level_%d.png lev3l_%d.png" % (pw,level,level,level-1,level-1))
```

You can probably tell that the script grew organically as more image transformations appeared.

After a long hour of unpacking archives, we reach level 1024 which only contains the flag.

Flag: `{FLG:p1xel0ut0fBound3xcept1on_tr4p_1s_shutt1ng_d0wn}`
