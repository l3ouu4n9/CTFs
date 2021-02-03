import string

def split_by_bits(char):
    result = []
    for _ in range(4):
        result.append(char & 0b11)
        char = char >> 2
    return result

def magic(val, inp):
    if val == 0b00:
        return (inp >> 3) | (inp << 5)
    elif val == 0b01:
        return (inp << 2) | (inp >> 6)
    elif val == 0b10:
        return inp + 0b110111
    else:
        return inp ^ 55


hashes = [182, 199, 159, 225, 210, 6, 246, 8, 172, 245, 6, 246, 8, 245, 199, 154, 225, 245, 182, 245, 165, 225, 245, 7, 237, 246, 7, 43, 246, 8, 248, 215]

mapping = {}
allowed = string.ascii_letters + "{}._!" + string.digits
for inp in allowed:
    inp = ord(inp)
    vals = split_by_bits(inp)
    res0 = magic(vals[0], inp) & 0xff
    res1 = magic(vals[1], res0) & 0xff
    res2 = magic(vals[2], res1) & 0xff
    res3 = magic(vals[3], res2) & 0xff
    mapping[res3] = inp


for h in hashes:
    print(chr(mapping[h]), end='')

# flag{v3ry1v3r1log1f14g1ch3ck3r!}
# but _ and 1 has the same value
# flag{v3ry_v3r1log_f14g_ch3ck3r!}