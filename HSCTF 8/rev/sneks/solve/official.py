#!/usr/bin/env python3
def nth_fib(n):
	""" uses fast doubling(see https://www.nayuki.io/page/fast-fibonacci-algorithms) """
	if n == 0:
		return 0
	elif n == 1 or n == 2:
		return 1
	x = nth_fib(n // 2)
	y = nth_fib(n // 2 + 1)
	if n % 2 == 0:
		return x * (2 * y - x)
	else:
		return x**2 + y**2

fibs = [nth_fib(n) for n in range(256)]
with open("output.txt") as f:
	nums = list(map(int, f.read().strip().split(" ")))
flag = bytearray()
for i, c in enumerate(nums):
	c //= 2
	c += 7**i
	c //= 5
	flag.append(fibs.index(c))
print(flag.decode())
