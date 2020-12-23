import requests

my_header = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarytjdF8LdcJlF9ZpQ7',
'Accept': '*/*',
'Origin': 'http://challs.xmas.htsp.ro:3003',
'Referer': 'http://challs.xmas.htsp.ro:3003/',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
'Cookie': 'PHPSESSID=47jb3u1oh62n4kkc8vp47sdkv6;',
'Connection': 'close'
}

state = '3132207c2030800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000048020000000000003133207c203133'
my_data = """
------WebKitFormBoundarytjdF8LdcJlF9ZpQ7
Content-Disposition: form-data; name="state"

{}
------WebKitFormBoundarytjdF8LdcJlF9ZpQ7
Content-Disposition: form-data; name="hash"

8ec4883990c9f7fc76f3514fcd5d4597
------WebKitFormBoundarytjdF8LdcJlF9ZpQ7
Content-Disposition: form-data; name="item_id"

2
------WebKitFormBoundarytjdF8LdcJlF9ZpQ7--
""".format(state.decode('hex'))[1:]

r = requests.Request('POST','http://challs.xmas.htsp.ro:3003/api/buy.php', headers=my_header, data=my_data)
prepared = r.prepare()

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

pretty_print_POST(prepared)

r = requests.post('http://challs.xmas.htsp.ro:3003/api/buy.php', headers=my_header, data=my_data)
print(r.text)

