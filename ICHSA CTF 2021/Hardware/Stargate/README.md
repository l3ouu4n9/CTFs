
# Stargate
## Description:
We found some Alien HW

You must help us find the password in order to save the world

Our specialists found 2 payloads:
1. The payload that the Aliens used to check the password (attached here)
2. HW sanity check payload (see our interactive HW access)

They also found that the payload structure is:

```C
struct data {
	uint16_t id;
	uint16_t type;
	uint16_t ???;
	uint16_t ???;
}
```

Interactive HW access: `nc stargates.ichsa.ctf.today 8006`

<img src="https://media2.giphy.com/media/l0Hly59i9w1fNGMh2/giphy.gif" width="448" height="252"/>

challenge author: [Aviv Cohen (zVaz)](https://twitter.com/_zVaz_)

