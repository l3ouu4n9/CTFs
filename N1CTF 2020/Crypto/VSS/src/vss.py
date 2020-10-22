#!/usr/bin/python3
import qrcode  # https://github.com/lincolnloop/python-qrcode
import random
import os
from PIL import Image
from flag import FLAG


def vss22_gen(img):
    m, n = img.size
    share1, share2 = Image.new("L", (2*m, 2*n)), Image.new("L", (2*m, 2*n))
    image_data = img.getdata()
    flipped_coins = [int(bit) for bit in bin(random.getrandbits(m*n))[2:].zfill(m*n)]
    for idx, pixel in enumerate(image_data):
        i, j = idx//n, idx % n
        color0 = 0 if flipped_coins[idx] else 255
        color1 = 255 if flipped_coins[idx] else 0
        if pixel:
            share1.putpixel((2*j, 2*i), color0)
            share1.putpixel((2*j, 2*i+1), color0)
            share1.putpixel((2*j+1, 2*i), color1)
            share1.putpixel((2*j+1, 2*i+1), color1)

            share2.putpixel((2*j, 2*i), color0)
            share2.putpixel((2*j, 2*i+1), color0)
            share2.putpixel((2*j+1, 2*i), color1)
            share2.putpixel((2*j+1, 2*i+1), color1)
        else:
            share1.putpixel((2*j, 2*i), color0)
            share1.putpixel((2*j, 2*i+1), color0)
            share1.putpixel((2*j+1, 2*i), color1)
            share1.putpixel((2*j+1, 2*i+1), color1)

            share2.putpixel((2*j, 2*i), color1)
            share2.putpixel((2*j, 2*i+1), color1)
            share2.putpixel((2*j+1, 2*i), color0)
            share2.putpixel((2*j+1, 2*i+1), color0)
    share1.save('share1.png')
    share2.save('share2.png')


def vss22_superposition():
    share1 = Image.open('share1.png')
    share2 = Image.open('share2.png')
    res = Image.new("L", share1.size, 255)
    share1_data = share1.getdata()
    share2_data = share2.getdata()
    res.putdata([p1 & p2 for p1, p2 in zip(share1_data, share2_data)])
    res.save('result.png')


def main():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=12,
        border=4,
    )
    qr.add_data(FLAG)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    vss22_gen(img._img)
    img.save('res.png')
    vss22_superposition()


if __name__ == '__main__':
    main()
