def second_question_function(a1, a2):
	return (12 * (a2 - 48) - 4 + 48 * (a1 - 48) - (a2 - 48)) % 10;


target = "7759406485255323229225"

myinput = "7"

for i in range(0, 21):
	
	assert len(myinput) == i + 1, print("No!! Did not find last one")
	print(f"{i+1}th charater")
	for j in range(0, 10):
		v1 = ord(str(j)) - 48

		output = (v1 + second_question_function(ord(target[i]), i + ord(target[i]))) % 10 + 48
		print(j, ord(chr(output)), ord(target[i+1]))
		if ord(target[i+1]) == output:
			print('get', i, chr(output))
			myinput += str(j)
			break
print("This should be my input", myinput)
# 7856445899213065428791