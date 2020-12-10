yes "GET / HTTP/1.1
" | nc -vv waf.balsnctf.com 8889 | rg BALSN | rg -v '_RED'