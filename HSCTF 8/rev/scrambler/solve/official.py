#!/usr/bin/env python3
import itertools
import random
from datetime import datetime

x = [
	't', 'Y', 'w', 'V', '|', ']', 'u', 'X', '_', '0', 'P', 'k', 'h', 'D', 'A', '4', 'K', '5', 'z',
	'Z', 'G', '7', ';', 'S', ' ', '/', '6', '%', '}', '\\', ',', ':', '>', '#', 'a', '$', '3', '`',
	'+', 'R', 'b', 'H', 'd', 's', '1', 'J', 'L', 'v', '9', '2', 'o', 'M', '<', 'e', '(', 'x', '-',
	'B', 'm', "'", 'y', 'Q', '"', 'W', 'l', '.', 'i', 'O', '^', 'p', '8', 'f', 'F', 'C', '?', 'g',
	'@', 'j', '[', 'r', '!', '=', 'E', '~', '*', 'T', '{', ')', 'U', 'N', 'c', '&', 'n', 'q', 'I'
]
with open("output.txt") as f:
	out = list(f.read().strip())
with open("chall.pyc", "rb") as f:
	f.seek(8)
	timestamp = int.from_bytes(f.read(4), byteorder="little")
	print(timestamp)
	print(datetime.fromtimestamp(timestamp))

for seed in itertools.count(timestamp):
	print(seed)
	random.seed(seed)
	s = out[:]
	for i in range(0, len(s), 2):
		s[i], s[i + 1] = s[i + 1], s[i]
	l = list(range(len(s)))
	random.shuffle(l)
	t = [""] * len(s)
	for i, j in enumerate(l):
		t[j] = s[i]
	s = t
	for _ in range(20):
		for i in range(len(s)):
			s[i] = chr(x.index(s[i]) + 32)
	s = "".join(s)
	if "flag" in s:
		print(s)
		break
