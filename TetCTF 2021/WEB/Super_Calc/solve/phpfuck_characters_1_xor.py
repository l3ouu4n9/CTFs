import sys

chars = "0123456789+-*/().~^|&"
new_chars = ""

if len(sys.argv) != 1:
    chars += sys.argv[1]


for i in chars:
    for j in chars: 
        # Xor
        c = chr(ord(i) ^ ord(j))
        if (not c in new_chars) and (c in "0123456789+-*/().~^|&abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_$[]"):
            print("(\'{}\'^\'{}\'):{}".format(i, j, c))
            new_chars += c

print(new_chars)