#!/usr/bin/env python3

import matplotlib.pyplot as plt
import cv2
import numpy as np
from collections import defaultdict

def read_and_plot(fname):
    img = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
    plt.title(fname)
    plt.imshow(img)
    plt.show()
    return img

i1_clr, i1_enc, i2_enc = map(read_and_plot, ["qr.png", "qr.encrypted.png", "flag.encrypted.png"])

# CONSTANTS
SIZE1 = 25 # number of QR-chunks in 1st image
SIZE2 = 29 # number of QR-chunks in the 2nd encrypted image

CHEIGHT = 16  # encryption chunk height
CHEIGHT2 = 22  # QR chunk height

FSIZE = CHEIGHT2 * SIZE2  # corrected size, so all chunks are equally big

def build_lookup(img_clr, img_enc, SIZE):
    """ build lookup dict from enc to clear strips (16 -> 16) and defaults to 128 """
    HEIGHT = img_clr.shape[0]  # image height/width in px
    CWIDTH = int(HEIGHT/SIZE)  # chunk width
    
    lookup = defaultdict(lambda: 128)
    for y in range(0, HEIGHT, CHEIGHT):
        for xpos in range(SIZE):
            x = int(xpos*(HEIGHT/SIZE) + CWIDTH/2)  # center line of a chunk
            block_enc = img_enc[y:y+CHEIGHT, x]
            block_clr = img_clr[y:y+CHEIGHT, x]
            lookup[tuple(block_enc)] = block_clr
    return lookup

def apply_lookup(img_enc, lookup, SIZE):
    """ apply lookup table and replace encrypted with cleartex chunks and unknown with 128 """
    HEIGHT = img_enc.shape[0]  # image height/width in px
    CWIDTH = int(HEIGHT/SIZE)  # chunk width

    # build image of 640 x 29 with looked up chunks
    img = np.zeros((HEIGHT, SIZE))
    for y in range(0, HEIGHT, CHEIGHT):
        for x in range(SIZE):
            xstart = int((x+0.5)*CWIDTH)
            block_enc = img_enc[y:y+CHEIGHT, xstart]
            img[y:y+16, x] = lookup[tuple(block_enc)]
    return img
    

def fix_qr(img, SIZE):
    """ fix unknown chunks by checking if the chunk contains the max value """
    img = cv2.resize(img, (SIZE, FSIZE))  # fix on the basis of qr-code chunks
    for y in range(0, FSIZE, CHEIGHT2):
        for x in range(0, SIZE):
            chunk = img[y:y+CHEIGHT2, x]
            img[y:y+CHEIGHT2, x] = 255 * (chunk.max() == 255)
    return cv2.resize(img, (SIZE, SIZE))  # resize to 29 x 29


def upscale(img, x=1, y=1): # repeat pixels x-times in x-dim and y-times in y-dim with kronecker-product
    return np.kron(img, np.ones((x, y)))

lookup = build_lookup(i1_clr, i1_enc, SIZE1)

img = apply_lookup(i2_enc, lookup, SIZE2)
big_img = upscale(img, 1, CHEIGHT2)


img = fix_qr(img, SIZE2)

big_img = upscale(img, CHEIGHT2, CHEIGHT2)
cv2.imwrite("flag.png", big_img);