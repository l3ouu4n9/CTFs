#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from math import sqrt
import os
import base64

def unchunkchunk(l):
    enc_merged = []
    for i in l:
        enc_merged += i
    return enc_merged


def chunkchunk(msg, l):
    return [msg[l * i:l * (i + 1)] for i in range(0, len(msg) // l)]


def pad(msg):
    r = int(sqrt(len(msg))) + 1
    head = base64.b64encode(os.urandom(r ** 2))[:r ** 2 - (len(msg))]
    msg = head + msg.encode('utf-8')
    msg = chunkchunk(msg, r)
    return [list(m) for m in msg]


def encrypt(A):
    row = len(A)
    col = len(A[0])
    top = 0
    left = 0
    tmp = []
    while (top < row and left < col):
        for i in range(left, col):
            tmp.append(A[top][i])
        top += 1
        for i in range(top, row):
            tmp.append(A[i][col - 1])
        col -= 1
        if (top < row):
            for i in range(col - 1, left - 1, -1):
                tmp.append(A[row - 1][i])
            row -= 1

        if (left < col):
            for i in range(row - 1, top - 1, -1):
                tmp.append(A[i][left])
            left += 1
    result = []
    for i in range(len(A)):
        r = []
        for j in range(len(A[0])):
            r.append(tmp[i * len(A[0]) + j])
        result.append(r)
    return result


def decrypt(A):
    row = len(A)
    col = len(A[0])
    top = 0
    left = 0
    col2 = 0
    row2 = 0
    tmp = [[0 for i in range(col)] for j in range(row)]
    while (top < row and left < col):
        for i in range(left, col):
            tmp[top][i] = A[col2][row2]
            row2 = row2 + 1 if row2 < len(A[0]) - 1 else 0
            col2 = col2 + 1 if row2 == 0 else col2
        top += 1
        for i in range(top, row):
            tmp[i][col - 1] = A[col2][row2]
            row2 = row2 + 1 if row2 < len(A[0]) - 1 else 0
            col2 = col2 + 1 if row2 == 0 else col2
        col -= 1
        if (top < row):
            for i in range(col - 1, left - 1, -1):
                # tmp.append(A[row - 1][i])
                tmp[row - 1][i] = A[col2][row2]
                row2 = row2 + 1 if row2 < len(A[0]) - 1 else 0
                col2 = col2 + 1 if row2 == 0 else col2
            row -= 1

        if (left < col):
            for i in range(row - 1, top - 1, -1):
                tmp[i][left] = A[col2][row2]
                row2 = row2 + 1 if row2 < len(A[0]) - 1 else 0
                col2 = col2 + 1 if row2 == 0 else col2
                # tmp.append(A[i][left])
            left += 1
    tmp = unchunkchunk(tmp)
    result = []
    for i in range(len(A)):
        r = []
        for j in range(len(A[0])):
            r.append(tmp[i * len(A[0]) + j])
        result.append(r)
    return result

enc = [[122, 83, 52, 67, 84, 70],
       [89, 114, 79, 48, 67, 125],
       [95, 121, 114, 53, 116, 55],
       [123, 95, 80, 51, 52, 95],
       [102, 115, 114, 95, 119, 107],
       [52, 117, 109, 33, 97, 112]]

for _ in range(len(enc)):
    enc = decrypt(enc)

flag = bytes(unchunkchunk(enc))
print('Flag: {}'.format(flag))