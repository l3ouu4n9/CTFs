#!/usr/bin/python3

import lc4

key = "igqehmd48pvxrl7k36y95j2sfnbo#wc_ztauT"
nonce = "fizz2swizz"
encrypted = "t4tmrvs9_k6vang76jj_rudxovvn6ar_zi4i8o3yqqql6eyannn_"
decrypted = lc4.decrypt(key, encrypted, nonce=nonce)
print(decrypted)