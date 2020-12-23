<?php
if (isset($_GET['source'])) {
  show_source("index.php");
  die ();
}

if (isset($_POST['flag'])) {
  include ("config.php");
  $conn = new mysqli($servername, $username, $password, $dbname);

  $query = "INSERT INTO FLAG (`id`, `n`) VALUES ";
  $alf = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!-_{}()";
  header('Ever wondered that Soy could be pronounced: like Soiii? Me neither.');

  for ($i=0; $i<strlen($_POST['flag']) && $i < 50; $i++) {
    $c = $_POST['flag'][$i];
    if (strlen($c) === 1) {
      $indx = strpos($alf, $c);
      if ($indx !== FALSE) {
        $query .= '(' . $i . ',"' . $alf[$indx] . '"),';
      } else {
        die("Invalid char.");
      }
    } else {
      die("Invalid input?");
    }
  }

  $query = substr($query, 0, strlen($query) - 1);
  mysqli_query($conn, 'DROP TABLE IF EXISTS FLAG');
  mysqli_query($conn, 'CREATE TABLE FLAG (`id` int not null primary key, `n` char)');
  mysqli_query($conn, $query);

  $query = "SELECT o FROM ( SELECT 0 v, '' o, 0 pc FROM (SELECT @pc:=0, @mem:='', @out:='') i UNION ALL SELECT v, CASE @pc WHEN 121 THEN 0 WHEN 70 THEN @pc:=73 WHEN 87 THEN IF(@x3 = 'a', 0, @pc:=89) WHEN 32 THEN  @sp := @sp + 1 WHEN 25 THEN @sp := @sp - 1 WHEN 28 THEN  @sp := @sp + 1 WHEN 56 THEN  @sp := @sp + 1 WHEN 18 THEN IF(BIN(ASCII(@prt)) NOT LIKE '1111011', @pc:=89, 0) WHEN 126 THEN 0 WHEN 17 THEN @prt := (SELECT n FROM FLAG WHERE id = 5) WHEN 12 THEN IF((SELECT n FROM FLAG WHERE id = 2) = 'M', 0, @pc:=80) WHEN 11 THEN IF(@count = @targetsz, 0, @pc:=89) WHEN 103 THEN  @sp := @sp + 1 WHEN 41 THEN IF(INSTR(@e, '?') > 0, 0, @pc:=43) WHEN 81 THEN (SELECT @x1 := n FROM FLAG WHERE id = 4) WHEN 49 THEN IF(SUBSTR(@dat, @i - 1, 3) NOT LIKE REVERSE('%tao%'), @pc:=124, 0) WHEN 73 THEN 0 WHEN 82 THEN (SELECT @x2 := n FROM FLAG WHERE id = 5) WHEN 58 THEN  @sp := @sp + 1 WHEN 92 THEN 0 WHEN 85 THEN (SELECT @x3 := n FROM FLAG WHERE id = 6) WHEN 64 THEN IF((SELECT FIELD((COALESCE((SELECT GROUP_CONCAT(n SEPARATOR '') FROM FLAG where id in (17, ASCII(@e)/3-3, (SELECT @xx := CEILING(ASCII(@f)/3)+1))), '78')), 'ATT', 'BXX', 'ENN', 'FPP', 'VMM', 'PSS', 'ZEE', 'YDD', 'PPP')) = FLOOR(@xx / 4), 0, @pc:=89) WHEN 95 THEN IF(@n = 0, 0, @pc:=99) WHEN 74 THEN @i := @i + 1 WHEN 68 THEN (SELECT @e := CONCAT_WS('AVION', (SELECT n FROM FLAG WHERE id = @i))) WHEN 78 THEN @out := @ok WHEN 107 THEN @sp := @sp - 1 WHEN 21 THEN  @sp := @sp + 1 WHEN 83 THEN IF(@x1 = 'd', 0, @pc:=89) WHEN 104 THEN @mem:=UpdateXML(@mem,'/m[$@sp]',CONCAT('<m>',@pc+2,'</m>')) WHEN 31 THEN @mem:=UpdateXML(@mem,'/m[$@sp]',CONCAT('<m>',@pc+2,'</m>')) WHEN 122 THEN @sp := @sp - 1 WHEN 102 THEN @mem:=UpdateXML(@mem,'/m[$@sp]',CONCAT('<m>',@n - 1,'</m>')) WHEN 45 THEN 0 WHEN 93 THEN @get_arg_tmp := @sp-2 WHEN 26 THEN @prt := (SELECT n FROM FLAG where id = 6) WHEN 86 THEN (SELECT @x4 := n FROM FLAG WHERE id = 7) WHEN 69 THEN IF(INSTR((SELECT IF(ORD(@e) = @i ^ 0x4c, @f, CHAR(@xx*2.75))), '?') = '0', 0, @pc:=71) WHEN 97 THEN @sp := @sp - 1 WHEN 59 THEN @mem:=UpdateXML(@mem,'/m[$@sp]',CONCAT('<m>',@pc+2,'</m>')) WHEN 108 THEN @sp := @sp - 1 WHEN 46 THEN @i := @i - 1 WHEN 115 THEN  @n:=ExtractValue(@mem,'/m[$@get_arg_tmp]') WHEN 100 THEN @mem:=UpdateXML(@mem,'/m[$@sp]',CONCAT('<m>',@n,'</m>')) WHEN 55 THEN @mem:=UpdateXML(@mem,'/m[$@sp]',CONCAT('<m>',@prt,'</m>')) WHEN 19 THEN @sp := 1 WHEN 24 THEN  @pc:=92 WHEN 33 THEN  @pc:=113 WHEN 29 THEN @mem:=UpdateXML(@mem,'/m[$@sp]',CONCAT('<m>',87,'</m>')) WHEN 16 THEN IF((@prt SOUNDS LIKE 'Soiii!'), 0, @pc:=80) WHEN 119 THEN IF(ASCII(@n) = @compareto, @pc:=121, 0) WHEN 3 THEN @notok := 'Wrong.' WHEN 42 THEN @pc:=45 WHEN 8 THEN IF(ASCII(@e) ^ 32 = 120, 0, @pc:=89) WHEN 98 THEN  @pc:=ExtractValue(@mem,'/m[$@sp]') WHEN 50 THEN (SELECT @i := GROUP_CONCAT(n SEPARATOR '') FROM FLAG Where id in (14, 16, 19, 22, 25, 32)) WHEN 91 THEN @pc:=126 WHEN 117 THEN  @compareto:=ExtractValue(@mem,'/m[$@get_arg_tmp]') WHEN 34 THEN @sp := @sp - 2 WHEN 84 THEN IF(@x2 = 'e', 0, @pc:=89) WHEN 37 THEN @i := 13 WHEN 20 THEN @mem:=UpdateXML(@mem,'/m[$@sp]',CONCAT('<m>',7,'</m>')) WHEN 63 THEN IF(@rv = INSTR('t35t', 'm4ch1n3'), @pc:=80, 0) WHEN 53 THEN IF(STRCMP((SELECT left(REPLACE(UNHEX(REPLACE(hex(RIGHT(QUOTE(MID(MAKE_SET(40 | 2,'Ook.','Ook?','Ook!','Ook?', 'Ook!','Ook?','Ook.'), 4)), 12)), '4F6F6B', '2B')), ',+', ''), 3)), (SELECT GROUP_CONCAT(n SEPARATOR '') FROM FLAG WHERE id > 28 and id < 32)) NOT LIKE '0', @pc:=89, 0) WHEN 111 THEN @sp := @sp - 1 WHEN 6 THEN IF(@dat = 'X-MAS', @pc:=80, 0) WHEN 80 THEN 0 WHEN 112 THEN  @pc:=ExtractValue(@mem,'/m[$@sp]') WHEN 120 THEN @rv := 0 WHEN 90 THEN @out := @notok WHEN 61 THEN  @pc:=113 WHEN 43 THEN 0 WHEN 30 THEN  @sp := @sp + 1 WHEN 101 THEN  @sp := @sp + 1 WHEN 52 THEN IF((SELECT IF(SUBSTR(@dat, (SELECT CEILING(ASCII(ASCII(@F))/2)), 3) = (SELECT NAME_CONST('TAO', 'SQL')), 1, 0)) = FIND_IN_SET(0,'f,e,e,d'), @pc:=124, 0) WHEN 71 THEN 0 WHEN 9 THEN IF((SELECT n FROM FLAG WHERE id = 1) = '-', 0, @pc:=89) WHEN 35 THEN IF(@rv = INSTR('xbar', 'foobar'), @pc:=80, 0) WHEN 62 THEN @sp := @sp - 2 WHEN 2 THEN @ok := 'OK.' WHEN 51 THEN IF(HEX(@i) = REPEAT('5F', 6), 0, @pc:=89) WHEN 88 THEN IF(@x4 = 'd', 0, @pc:=89) WHEN 109 THEN  @n:=ExtractValue(@mem,'/m[$@sp]') WHEN 10 THEN (SELECT @count := COUNT(*) FROM FLAG) WHEN 1 THEN @strn := 'MySQL' WHEN 39 THEN 0 WHEN 96 THEN @rv := 1 WHEN 106 THEN  @pc:=92 WHEN 114 THEN @get_arg_tmp := @sp-3 WHEN 47 THEN IF(@i > 10, @pc:=39, 0) WHEN 0 THEN @mem:=CONCAT(@mem,REPEAT('<m></m>',50)) WHEN 94 THEN  @n:=ExtractValue(@mem,'/m[$@get_arg_tmp]') WHEN 60 THEN  @sp := @sp + 1 WHEN 99 THEN 0 WHEN 123 THEN  @pc:=ExtractValue(@mem,'/m[$@sp]') WHEN 89 THEN 0 WHEN 38 THEN @l := 0 WHEN 113 THEN 0 WHEN 36 THEN IF((SELECT ELT(BIT_LENGTH(BIN(12))/32, BINARY(RTRIM(CONCAT(REVERSE(repeat(SUBSTR(REGEXP_REPLACE(HEX(weight_string(TRIM(UCASE(TO_BASE64((SELECT CONCAT((SELECT n FROM FLAG WHERE id LIKE '20'), (SELECT n FROM FLAG where id IN ('50', '51', SUBSTR('121', 2, 2)))))))))), 'D', 'A'), -16, 16), 1)), (SELECT SPACE(6))))))) = CONCAT_WS('00','A3','43','75','A4',''), 0, @pc:=89) WHEN 13 THEN (SELECT @f := n FROM FLAG WHERE id = 3) WHEN 44 THEN @l := 1 WHEN 65 THEN @i := 33 WHEN 48 THEN IF(@l > FIND_IN_SET('x','a,b,c,d'), @pc:=89, 0) WHEN 110 THEN @rv := @rv * @n WHEN 125 THEN @out := @notok WHEN 127 THEN 0 WHEN 4 THEN @targetsz := 42 WHEN 5 THEN (SELECT @dat := COALESCE(NULL, NULL, GROUP_CONCAT(n SEPARATOR ''), 'X-MAS') FROM FLAG) WHEN 116 THEN @get_arg_tmp := @sp-2 WHEN 23 THEN  @sp := @sp + 1 WHEN 105 THEN  @sp := @sp + 1 WHEN 22 THEN @mem:=UpdateXML(@mem,'/m[$@sp]',CONCAT('<m>',@pc+2,'</m>')) WHEN 15 THEN @prt := CONCAT((SELECT n FROM FLAG WHERE id = 4), (SELECT n FROM FLAG WHERE id = 7), (SELECT n FROM FLAG WHERE id = 24)) WHEN 14 THEN IF(ASCII(@e) + ASCII(@f) = 153, 0, @pc:=89) WHEN 54 THEN @prt := (SELECT n FROM FLAG whEre id in (CAST((SUBSTR(REPEAT(RPAD(SOUNDEX('doggo'), 2, '?'), 2), 4, 1)) AS INTEGER) * 7 + 1)) WHEN 72 THEN @l := @l + 1 WHEN 77 THEN 0 WHEN 118 THEN @rv := 1 WHEN 27 THEN @mem:=UpdateXML(@mem,'/m[$@sp]',CONCAT('<m>',@prt,'</m>')) WHEN 76 THEN IF(@l > LOCATE(FIND_IN_SET('p','abcdefghijklmnoqrstuvwxyz'), '1'), @pc:=124, 0) WHEN 7 THEN (SELECT @e := n FROM FLAG WHERE id = 0) WHEN 40 THEN (SELECT @e := CONCAT((SELECT n FROM FLAG WHERE id = @i))) WHEN 79 THEN @pc:=126 WHEN 124 THEN 0 WHEN 66 THEN @l := 0 WHEN 57 THEN @mem:=UpdateXML(@mem,'/m[$@sp]',CONCAT('<m>',52,'</m>')) WHEN 67 THEN 0 WHEN 75 THEN IF(@i < 41, @pc:=67, 0) ELSE @out END, @pc:=@pc+1 FROM (SELECT (E0.v+E1.v+E2.v+E3.v+E4.v+E5.v+E6.v+E7.v+E8.v+E9.v+E10.v) v FROM(SELECT 0 v UNION ALL SELECT 1 v) E0 CROSS JOIN (SELECT 0 v UNION ALL SELECT 2 v) E1 CROSS JOIN (SELECT 0 v UNION ALL SELECT 4 v) E2 CROSS JOIN (SELECT 0 v UNION ALL SELECT 8 v) E3 CROSS JOIN (SELECT 0 v UNION ALL SELECT 16 v) E4 CROSS JOIN (SELECT 0 v UNION ALL SELECT 32 v) E5 CROSS JOIN (SELECT 0 v UNION ALL SELECT 64 v) E6 CROSS JOIN (SELECT 0 v UNION ALL SELECT 128 v) E7 CROSS JOIN (SELECT 0 v UNION ALL SELECT 256 v) E8 CROSS JOIN (SELECT 0 v UNION ALL SELECT 512 v) E9 CROSS JOIN (SELECT 0 v UNION ALL SELECT 1024 v) E10 ORDER BY v) s) q ORDER BY v DESC LIMIT 1";

  mysqli_query($conn, $query, MYSQLI_USE_RESULT);
  $result = mysqli_query($conn, $query, MYSQLI_USE_RESULT);
  echo mysqli_fetch_array ($result, MYSQLI_ASSOC)['o'];
  die();
}
?>

<!DOCTYPE html>
<html><head>
<meta http-equiv="content-type" content="text/html; charset=windows-1252"><meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.64">
<meta http-equiv="Cache-control" content="public, min-fresh:2400000">
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
<style type="text/css"> html { max-width:1024px;overflow:auto;} </style>
<script type="text/javascript" async="" src="christmas7_data/ga.js"></script><script language="JavaScript" type="text/javascript">
if (window == top) { 
//document.write('<div style="height:30px;"></div><div id="content" style="max-width:1022px;overflow:auto">');
}
else {document.write('<div id="content" style="max-width:804px;overflow:auto">');} </script></head><body vlink="#009900" text="#000000" link="#FF0000" bgcolor="#FFFFFF" background="christmas7_data/snow.jpg" alink="#FF0000"><div id="content" style="max-width:804px;overflow:auto">

<script language="JavaScript" src="geovck08.js"></script>



   <meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
   <meta name="Author" content="Joanne">
   <meta name="GENERATOR" content="Mozilla/4.08 [en] (Win95; I) [Netscape]">
   <title>Christmas Midis</title>



&nbsp;
<br>&nbsp;
<center><table cols="1" width="95%" cellspacing="10" cellpadding="10" border="0">
<caption><font size="+4">Christmas Midis</font></caption>

<tbody><tr>
<td>
<center><img src="christmas7_data/asan7x.gif" width="104" height="121"><img src="christmas7_data/asan7.gif" width="111" height="115" border="0"></center>
</td>
</tr>
<tr>
<td>
<center><font size="+1">Christmas Medley</font>
<br><embed src="christmas7_data/medley1.mid" autostart="TRUE" width="146" height="60">
<br>Right Click for Controls</center>
</td>
</tr>

<tr style="text-align: center;">
<td>
<h1>Ho! Ho! Ho! Verify your flag!</h1>
<form action="/index.php" method="post">
  <input type="text" name="flag"><br>
  <input type="submit" value="Submit">
</form>
</td>
</tr>

<tr>
<td>
<center><font size="+2"><a href="https://www.oocities.org/jjdox/Christmas/apply-graphics.html#Sound">How to Add Sound
to your Web Page.</a></font>
<br><font size="+2">Click on each title below to hear the midi</font></center>
</td>
</tr>
</tbody></table></center>


<center><table cols="4" width="95%" cellspacing="5" cellpadding="5" border="">
<caption>
<center><font size="+3">Carols</font></center>
</caption>

<tbody><tr>
<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/3kings.mid">We Three Kings</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/bethlehem.mid">Oh Little Town of Bethlehem</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/douhear.mid">Do You Hear What I Hear?</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/drummer.mid">Little Drummer Boy</a></font></center>
</td>
</tr>

<tr>
<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/faithful.mid">Oh Come All Ye Faithful</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/hark.mid">Hark the Herald Angels Sing</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/holynight.mid">Oh Holy Night</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/joyworld1.mid">Joy to the World</a></font></center>
</td>
</tr>

<tr>
<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/manger.mid">Away in the Manger</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/midnight.mid">It Came upon a Midnight Clear</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/silnight1.mid">Silent Night</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/whatchild.mid">What Child is This?</a></font></center>
</td>
</tr>
</tbody></table></center>

<center><table cols="4" width="95%" cellspacing="5" cellpadding="5" border="">
<caption>
<center><font size="+3">Traditional &amp; Novelty Songs</font></center>
</caption>

<tbody><tr>
<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/12days.mid">The 12 Days of Christmas</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/blgrjb.mid">Blue Grass Jingle Bells</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/carolbells.mid">Carol Bells</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/chestnuts.mid">Chestnuts Roasting on an
Open Fire</a></font></center>
</td>
</tr>

<tr>
<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/xmastree.mid">Oh! Christmas Tree</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/deckhall.mid">Deck the Halls</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/feliz.mid">Feliz Navada</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/frosty.mid">Frosty the Snowman</a></font></center>
</td>
</tr>

<tr>
<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/gramma.mid">Gramma Got Run Over by a Reindeer</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/happychr.mid">Happy Christmas</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/hollyjoll1.mid">Holly Jolly Christmas</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/homefor.mid">I'll be Home for the Holidays</a></font></center>
</td>
</tr>

<tr>
<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/homehol.mid">There's No Place Like Home
for the Holidays</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/housetop.mid">Up on the Housetop</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/JBrock1.mid">Jingle Bell Rock</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/jingle.mid">Jingle Bells</a></font></center>
</td>
</tr>

<tr>
<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/kissing.mid">I Saw Mommy Kissing Santa Claus</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/letsnow.mid">Let it Snow</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/littlexmas.mid">Have Yourself a Merry Little
Christmas</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/rocking.mid">Rocking Around the Christmas
Tree</a></font></center>
</td>
</tr>

<tr>
<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/rudolph.mid">Rudolph</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/Sccoming1.mid">Santa Claus is Coming to
Town</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/silbells.mid">Silver Bells</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/sleighride2.mid">Sleigh Ride</a></font></center>
</td>
</tr>

<tr>
<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/whchrist.mid">White Christmas</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/winterwon.mid">Winter Wonderland</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/wishmerry1.mid">We Wish You a Merry Christmas</a></font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/happyjoy.wav">Happy Happy Joy Joy</a> (wav
file)</font></center>
</td>
</tr>
</tbody></table></center>

<center><table cols="4" width="95%" cellspacing="5" cellpadding="5" border="">
<caption>
<center><font size="+3">Nutcracker Suite</font></center>
</caption>

<tbody><tr>
<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/nutcrack.mid">Overture</a></font>
<br><font size="+1">(Ouverture)</font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/nutcrack1.mid">March of the Toy Soldiers</a>
(Marche)</font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/nutcrack4.mid">Waltz of the Flowers </a>(Valse
des Fluers)</font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/nutcrack2.mid">Chinese Dance</a></font>
<br><font size="+1">(Danse Chinoise)</font></center>
</td>
</tr>

<tr>
<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/nutcrack3.mid">Miltitons Dance</a></font>
<br><font size="+1">(Danse de Miltitons)</font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/nutcrack5.mid">Arabian Dance</a></font>
<br><font size="+1">(Danse Arabe)</font></center>
</td>

<td>
<center><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/sugarplum.mid">Dance of the Sugar Plum Fairy
</a>(Danse
de la Fee-Dragee)</font></center>
</td>

<td><font size="+1"><a href="https://www.oocities.org/jjdox/Christmas/reedpipe.mid">Reed Pipe Dance</a></font></td>
</tr>
</tbody></table></center>

<center>
<p>[<a href="https://www.oocities.org/jjdox/Christmas/christmas.html">Christmas Index</a>] [<a href="https://www.oocities.org/jjdox/Christmas/christmas2.html">Animated
Graphics</a>] [<a href="https://www.oocities.org/jjdox/Christmas/christmas3.html">More Animated Graphics</a>]
<br>[<a href="https://www.oocities.org/jjdox/Christmas/christmas4.html">Christmas Dividers</a>] [<a href="https://www.oocities.org/jjdox/Christmas/christmas5.html">Santas</a>]
[<a href="https://www.oocities.org/jjdox/Christmas/christmas6.html">Non-animated Graphics</a>] [Midis] [<a href="https://www.oocities.org/jjdox/Christmas/christmas8.html">Backgrounds</a>]</p></center>

<br>&nbsp;
<p><br>
<br>
</p></div><style> 
.zoomout { -webkit-transition: -webkit-transform 0.5s ease;
-moz-transition: -moz-transform 0.5s ease;
-o-transition: -o-transform 0.5s ease;
transition: transform 0.5s;
-ms-transition: transform 0.5s ease;}
.zoomin { 
filter: blur(0)
-webkit-transform: scaleY(1.15);
-moz-transform: scaleY(1.15);
-o-transform: scaleY(1.15);
transform: scaleYY(1.15);
-ms-transform: scaleY(1.15);
} 
#archive:hover { zoom:101%;)
</style>

<script language="JavaScript" type="text/javascript">
var width  = window.innerWidth || (window.document.documentElement.clientWidth ||  window.document.body.clientWidth);
var height = window.innerHeight || (window.document.documentElement.clientHeight || window.document.body.clientHeight);
var d = document;

</script>
<script type="text/javascript">
if (x<=1015){d.getElementById('foot').style.left = x + "px";}
d.getElementById('footer').style.left = x + d.getElementById('foot').offsetWidth + "px";
</script>

<!-- ?source=1 -->
</body></html>