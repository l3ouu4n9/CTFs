# It's wasm time


## Steps
* download wasm file
* convert into c, `wasm2c uctf_check.wasm -o uctf_check.c`
* find flag length using ghidra, it's 40
* find hash values and location of computed hashes
* hook memcpy function and print values in computed hashes range
* write main function to call Z_check_flagZ_iii
* compile, `gcc -o bin main.c uctf_check.c /usr/share/doc/wabt/examples/wasm2c/wasm-rt-impl.c -I /usr/share/doc/wabt/examples/wasm2c/ -m32`
* figure out that hashes are checked in reverse order and depends on previous chars (?)
* write bruteforce script


## Solver script
```python
import subprocess
hashes = [3376432092, 3148712937, 1092076640, 3085618703, 1307668188, 3064531694, 3095200819, 1314007355, 1606225393, 1858895620, 2335139813, 3037063580, 1259113065, 3219670873, 938526970, 969196095, 1671119862, 4272550096, 269800838, 522471065, 294751910, 2811768691, 1081432078, 1783355845, 4021686844, 18937586, 4043001627, 1741576394, 4258593175, 1720489385, 1751158510, 2453082277, 2213928557, 1943025302, 2644949069, 866998554, 347023697, 2340565760, 4097429266, 55132197]

FINAL_LEN = 40
CURRENT_CHAR = FINAL_LEN - 1
FLAG = ["A"] * FINAL_LEN

CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!_{}-"
for _ in range(FINAL_LEN):
    for c in CHARS:
        FLAG[CURRENT_CHAR] = c
        flag = "".join(FLAG)
        output = int(subprocess.check_output(f"echo '{flag}' | /tmp/bin | grep '^{CURRENT_CHAR}:'", shell=True).split()[-1].strip().split(b":")[-1])
        if output == hashes[CURRENT_CHAR]:
            print(CURRENT_CHAR, flag)
            CURRENT_CHAR -= 1
```

## Main
```c
#include "uctf_check.h"
#include <stddef.h>
#include <stdio.h>
int main(int argc, char** argv) {
  init();
  u32 *ptr = *(u32 *)Z_memory + 0x1000;
  scanf("%40s", ptr);
  u32 result = Z_check_flagZ_iii(0x1000, 40);
  return result;
}
```

### memcpy hooking
```c
void *Hook_memcpy(void *dest, const void *src, size_t n) {
        if(dest >= *(u32 *)&memory + 0x000f3fd8 && dest <= *(u32 *)&memory + 0x000f3fd8 + 40 * 4) {
                printf("%d:%u\n", ((u32)dest-0x000f3fd8 - *(u32 *)&memory)/4, *(u32 *)src);
        }
        return memcpy(dest, src, n);
}

#define memcpy(a, b, c) Hook_memcpy(a, b, c)
```