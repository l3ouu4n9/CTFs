
# sauerbraten
## Description:
We love [Cube 2: Sauerbraten](http://sauerbraten.org/) so much that we decided to host a server so you could enjoy some gaming during the CTF.

Become an admin of the server (>= PRIV_ADMIN) and then send `getflag` in the game chat to retrieve the flag.

To spin up the server you should connect to this port and solve the PoW:

`nc 46.101.74.209 1337`

**2021-02-20 03:20 UTC**: If Sourceforge is down, you can get an up-to-date version of the source code [from Github](https://github.com/tomatenquark/sauerbraten_code/tree/010d533696a454eaa404cc4691d9a466643a0983).

**2021-02-20 20:22 UTC**. Hint: there's a memory corruption bug in `parsepacket`.

Author: mrtumble

