# Fancy Caesar Cipher
We RSA encrypted the flag, but forgot to save the private key. Is it possible to recover the flag without it? 

## Writeup
We are given `n, e, and c`. The thing to notice is that `c` is encrypted character by character. We can take it as some kind of easy block cipher.

By encrypting all the printables and compare them with the cipher text one by one, we can get the flag.