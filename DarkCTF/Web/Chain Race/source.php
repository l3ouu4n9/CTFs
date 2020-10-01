<?php
session_start();
include 'flag.php';

$login_1 = 0;
$login_2 = 0;

if(!(isset($_GET['user']) && isset($_GET['secret']))){
    highlight_file("index.php");
    die();
}

$login_1 = strcmp($_GET['user'], "admin") ? 1 : 0;

$temp_name = sha1(date("ms").@$_COOKIE['PHPSESSID']);
session_destroy();
if (($_GET['secret'] == "0x1337") || $_GET['user'] == "admin") {
    die("nope");
}

if (strcasecmp($_GET['secret'], "0x1337") == 0){
    $login_2 = 1;
}

file_put_contents($temp_name, "your_fake_flag");

if ($login_1 && $login_2) {
    if (@unlink($temp_name)) {
        die("Nope");
    }
	echo $flag;
}
die("Nope");