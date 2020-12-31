<?php

// Web02 Challenge "Russian Doll"

include('flag.php');

error_reporting(0);

if(!isset($_GET['text'])){
    highlight_file(__FILE__);
    die();
}


// Stage 1
$text = $_GET['text'];
if(@file_get_contents($text)!=="Привет хакер"){
        die("You must speak my language a different way!");
}

echo "Stage 1 is complete! You unlocked the key: " . $secretkey . "\n";

// Stage 2
$key1 = $_GET['key1'];
$keyId = 1337;

if (intval($key1) !== $keyId || $key1 === $keyId) {
    die("хаха, это строго не сработает");
}

echo "Stage 2 is complete! Keep Going!\n";

// Stage 3
$hash = $_GET['hash'];
$token = time();
$tokenDeath = $token + 24*60*60;

if (($tokenDeath - time()) <= 0) {
    if(substr(hash("sha256", $keyId + $token . $secretkey), 5, 25) == $hash) {
        $keyId = $_GET['keyId'];
    }
} else {
    die("Ваш токен мертв, как и эта попытка");
}

echo "Stage 3 is complete! You defeated death, for now...\n";


// Stage 4
$key2 = 69;
if(substr($keyId, $key2) !== sha1($keyId)){
    die("ты не можешь сдаться сейчас!");
}

echo "Stage 4 is complete! Almost there!\n";

// Final Stage
assert_options(ASSERT_BAIL, 1);
assert("$sixnine == $keyId");

echo "Final stage is complete Where da flag homie? 💩\n";
// echo $flag;