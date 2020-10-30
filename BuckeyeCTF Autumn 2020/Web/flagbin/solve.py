import requests
from bs4 import BeautifulSoup

r = requests.get('http://pwn.osucyber.club:13370/sitemap.xml')
soup = BeautifulSoup(r.text, 'html.parser')

loc_tags = soup.find_all('loc')
for loc_tag in loc_tags:
	r = requests.get(loc_tag.text)
	if 'osuctf{' in r.text:
		print(loc_tag.text)
		print(r.text)
		print('')