
# Pincrack
## Description:
A classic crackme.

libcrypt and libscrypt are required. On Debian-based system :
- `# apt update`
- `# apt install libcrypt1 libscrypt-kdf1`

If a packaged version of libscrypt is not available for your system,
the library used to build the binary is given.
Usage :
- `$ LD_PRELOAD=./libscrypt-kdf.so.1.0.0 ./pincrack ...`

**Files :**
- [pincrack](https://challenges.thcon.party/reverse-dec1be1-pincrack/pincrack)
- [libscrypt-kdf.so.1.0.0](https://challenges.thcon.party/reverse-dec1be1-pincrack/libscrypt-kdf.so.1.0.0)

**Creator :**
dec1be1 (Discord : dec1be1#7849)

