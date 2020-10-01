# Maelstrom
Can you decrypt the flag?

## Writeup
Take a deep look to the functions, `x` is a function to check if a given number is a prime, and `num` becomes `(2 ** num) - 1` in function `z`.

This is `Mersenne prime`. Since the length of `cipher` is 21, I use the first 21 `p` that can make M<sub>p</sub>

Run the python script without the check `if x(z(num))`, and got the flag.