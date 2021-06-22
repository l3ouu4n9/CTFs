list = [0, 1, 98, 1, 48, 1, 3, 1, 3, 5, 45, 1, 5, 1, 17, 1, 1, 5, 3, 2, 6, 3, 4, 17, 1, 6, 1, 2, 7, 1, 1, 5, 1, 1, 1, 2, 1, 12, 2, 9, 7, 1, 1, 5, 4, 2, 11, 2, 1, 1, 2, 1, 7, 2, 1, 111, 2, 2, 1, 11, 2, 1, 9, 3, 3, 1, 7, 9, 3, 1384, 15, 3, 2, 4, 1, 3, 2, 3, 1, 9, 1, 2, 7, 1, 3, 73, 1, 1, 7, 1, 1, 6, 13, 1, 1, 1, 12, 1, 3, 1, 6, 18, 1, 21, 1, 2, 4, 1, 1, 8, 1, 6, 1, 1, 1, 1, 1, 12, 4, 7, 1, 1, 8, 5, 2, 1, 2, 3, 2, 1, 1, 5, 1, 21, 2, 2, 1, 6, 2, 208, 2, 7, 4, 2, 8, 1, 2, 2, 2, 5, 10, 5, 2, 5, 1, 5, 1, 7, 2, 1, 13, 2, 9, 4, 1, 2, 2, 5, 5, 1, 2, 20, 1, 2, 1, 2, 2, 7, 1, 6, 11, 2, 2, 2, 3, 1, 3, 1, 37, 1, 3074, 15, 5, 1, 2, 1, 2, 7, 2, 2, 2, 2, 1, 60, 1, 8, 2, 1, 4, 14, 1, 10, 1, 2]

cf = continued_fraction(list) # constructs continued fraction object
R = RealField(1000) # 1000 digits of precision
d = R(cf.value()) # decimal
s = str(d)
s = s[2:s.find('000')] # crops the decimal from the decimal point to the start of null bytes

ss = ""
while len(s) > 0: # interprets the string as a concatenation of decimal ascii values
    if s[0] == '1':
        ss += chr(int(s[0:3]))
        s = s[3:]
    else:
        ss += chr(int(s[0:2]))
        s = s[2:]
print(ss)

# sage official.sage
# bcactf{c0nv3rg3d_0r_n3v3r3nd1ng?_jvnai23b15cxkl}