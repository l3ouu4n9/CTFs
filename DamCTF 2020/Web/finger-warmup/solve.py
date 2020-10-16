import requests
from bs4 import BeautifulSoup

base_url = 'https://finger-warmup.chals.damctf.xyz/'
href = ''

while True:
	print("Access " + base_url + href)
	r = requests.get(base_url + href)
	soup = BeautifulSoup(r.text, 'html.parser')
	try:
		href = soup.find('a').get('href')
	except:
		print(soup)
		break