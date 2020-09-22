import string

enc = "Ypw'zj zwufpp hwu txadjkcq dtbtyu kqkwxrbvu! Mbz cjzg kv IAJBO{ndldie_al_aqk_jjrnsxee}. Xzi utj gnn olkd qgq ftk ykaqe uei mbz ocrt qi ynlu, etrm mff'n wij bf wlny mjcj :)."
decrypt = ""

shift = 0
for ch in enc:
	if ch in string.ascii_lowercase:
		decrypt += chr(((ord(ch) - 97 - shift) % 26 ) + 97)
	elif ch in string.ascii_uppercase:
		decrypt += chr(((ord(ch) - 65 - shift) % 26 ) + 65)
	else:
		decrypt += ch
	shift = (shift + 1) % 26

print(decrypt)