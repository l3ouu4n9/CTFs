
nums = [3, 14, 6, 6, 10, 2, 5, 17, 22, 6, 7, 10, 18, 25, 25, 22, 16, 24, 25, 2, 6, 18, 6, 16, 7, 2]

password = ''
for num in nums:
	password += chr((num + 12) % 26 + ord('a'))
print(password)