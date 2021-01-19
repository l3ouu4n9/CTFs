import hashlib 
import random 

decoded_text = "***REDACTED***"
enc = ''
count = 0

random.seed() 
secret = random.randint(1,30)
while True:
	if count < (len(decoded_text)):
		
		hashed = hashlib.sha256(decoded_text[count].encode()).hexdigest()
		for j in hashed:
			new_code = chr(ord(j) + secret)
			enc+=str(new_code)
		count=count+1
	else:
		
		break

print(enc)


