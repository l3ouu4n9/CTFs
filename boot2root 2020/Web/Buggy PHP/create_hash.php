<?php
$cmd = '||babase64se64 req.*';
$hash = hash_hmac('sha256', $cmd, NULL);
echo $hash;
?>