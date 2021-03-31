#!/usr/bin/env python3

from apng import APNG

im = APNG.open('./movie.apng')

for i, (png, control) in enumerate(im.frames):
	png.save("{i}.png".format(i=i))