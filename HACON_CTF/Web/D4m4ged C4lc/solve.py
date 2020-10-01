import requests
import base64

url = 'https://hidden-journey-18965.herokuapp.com/'

flag_b64 = ''
for i in range(1, 5):
	page = 'page' + str(i)
	r = requests.post(url + page, data={'value':'3'})
	assert r.status_code == 200

	flag_b64 += r.text.split('>')[1].strip()

print(base64.b64decode(flag_b64))