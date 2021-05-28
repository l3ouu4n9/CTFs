from pwn import *

target = remote("java.sdc.tf", 1337)

# Find a nonzero `long x` such that `x == -x`
# overflow
target.recvuntil("x =", timeout=5)
target.sendline("-9223372036854775808")

# Find 2 different `long` variables `x` and `y`, differing by at most 10, such that `Long.hashCode(x) == Long.hashCode(y)`
# hash xors the upper and lower 32 bits of long
# so all 1s for a number (-1) and all 0s for the other (0) will result in the same hash
target.recvuntil("x =", timeout=5)
target.sendline("0")
target.recvuntil("y =", timeout=5)
target.sendline("-1")

"""
Enter a `float` value `f` that makes the following function return true:
boolean isLucky(float magic) {
    int iter = 0;
    for (float start = magic; start < (magic + 256); start++) {
        if ((iter++) > 2048) {
            return true;
        }
    }
    return false;
}
"""
# we needed a float with bit-conversion error abs(Err) > 1 to loop forever
# hard part was to get it in under 7 chars
# then you remember that "e" was created
# and you get hyped for your first flag
target.recvuntil("f =", timeout=5)
target.sendline("9.002e7")
# target.sendline("1e+8")

# flag 1
target.recvuntil("flag:")
flag = target.recvuntil("}").decode().replace("\n", "")
print(f'Flag 1: {flag}')

"""
Enter 3 `String` values `s1`, `s2`, and `s3` such that:
new BigDecimal(s1).add(new BigDecimal(s2)).compareTo(new BigDecimal(s3)) == 0
but
Double.parseDouble(s1) + Double.parseDouble(s2) != Double.parseDouble(s3)
"""
# an example i found while googling BigDecimal VS parseDouble :o
# can't remember which link
target.recvuntil("s1", timeout=5)
target.sendline("0.03")
target.recvuntil("s2", timeout=5)
target.sendline("-0.04")
target.recvuntil("s3", timeout=5)
target.sendline("-0.01")
"""
target.recvuntil("s1", timeout=5)
target.sendline("1e+1000")
target.recvuntil("s2", timeout=5)
target.sendline("-1e+1000")
target.recvuntil("s3", timeout=5)
target.sendline("0")
"""

"""
Fill in <type>, <num1>, <num2> below:
var i = (<type>) <num1>; var j = (<type>) <num2>;
such that after running the code above, the following expression:
i < j || i == j || i > j
evaluates to `false`.
<num1> and <num2> are Java code that satisfies this regex: [0-9]*\.?[0-9]*
"""
# part1: surprinsingly easy concept, objects in Java don't use ==
# for example Strings use compareTo()
# i knew Strings would work, but i was very dumb to forget that Integer is not Int
# and that Integer is also an Object
# so it would behave like Strings
# part2: you need to make use of the caching trick
# Integer caches values [-127:127] for performance
# so use 128 or larger
target.recvuntil("<type>:", timeout=10)
target.sendline("Integer")
target.sendline("128")
target.sendline("128")
"""
target.sendline("Double")
target.sendline("1.0")
target.sendline("1.0")
"""

# flag 2
target.recvuntil("flag:")
flag = target.recvuntil("}").decode().replace("\n", "")
print(f'Flag 2: {flag}')



# Flag 1: sdctf{JAVA_Ar1thm3tIc_15_WEirD}
# Flag 2: sdctf{MATH_pr0f:iS_tH1S_@_bUG?CS_prOF:n0P3_tHIS_iS_A_fEATuRe!}