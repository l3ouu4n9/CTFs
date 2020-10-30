def ValidatePassword(password):
    print("Password Validator v1.0")
    print("Attempting to validate password...")

    if(len(password[::-2]) != 12 or len(password[17:]) != 7):
        print("Woah, you're not even close!!")
        return False

    pwlen = len(password)
    chunk1 = 'key'.join([chr(0x98 - ord(password[c]))
                             for c in range(0, int(pwlen / 3))])
    if "".join([c for c in chunk1[::4]]) != '&e"3&Ew*':
        print("You call that the password? HA!")
        return False

    chunk2 = [ord(c) - 0x1F if ord(c) > 0x60
                  else (ord(c) + 0x1F if ord(c) > 0x40 else ord(c))
                  for c in password[int(pwlen / 3) : int(2 * pwlen / 3)]]
    ring = [54, -45, 9, 25, -42, -25, 31, -79]
    for i in range(0, len(chunk2)):
        if(0 if i == len(chunk2) - 1 else chunk2[i + 1]) != chunk2[i] + ring[i]:
            print("You cracked the passwo-- just kidding, try again! " + str(i))
            return False

    chunk3 = password[int(2 * pwlen / 3):]
    code = 0xaace63feba9e1c71ef460e6dbf1b1fbabfd7e2e35401440ac57e93bd9ba41c4fbd5d437b1dfab11fe7a1c6c2035982a71765fc9a7b32ccef695dffb71babe15733f5bb29f76aae5f80fff
    valid = True
    for i in range(0, len(chunk3)):
        if(ord(chunk3[i]) < 0x28):
            valid = False
        code -= (257 ** (ord(chunk3[i]) - 0x28)) * (1 << i)

    if code == 0 and valid:
        print("Password accepted!")
        return True
    else:
        print("Quite wrong indeed!")
        return False

print("Please enter password")
while not ValidatePassword(input()):
    pass
