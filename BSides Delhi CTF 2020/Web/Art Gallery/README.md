## Chall Name : Art Gallery

### Description: 
my friend's art gallery is still in process. I'm helping him to buid a website to sell his works, so please don't mess with things yet (Ofcourse i have my plans to stop you too) 

## Link
http://65.0.54.62/

## Flag
BSDCTF{1_see_u_dumped_the_database}

### brief - solution:

 - use the test credentials to login (from the page source)
 - exploit the order by in sql query and do blind sql injection 
 - bypass waf and dump the database(script to extract table name, column name and flag)
 - full solution refer solution.py
