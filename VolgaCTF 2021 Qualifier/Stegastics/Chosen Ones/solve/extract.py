#!/usr/bin/env python3

import cv2 as cv
import matplotlib.pyplot as plt
from bitstring import BitStream, BitArray

with open("out.zip", "wb") as f:
    for name in ["images/437.png", "images/579.png"]:
        img = cv.imread(name)
        blue_plane = img[:,:,0] & 1 # get LSB from 0'th channel (blue)
        bits = "".join(blue_plane.flatten().astype(str))  # flatten 1920x1080 array of 0/1 to string
        by = BitArray(bin=bits).tobytes()  # bitstring to bytes
        f.write(by)