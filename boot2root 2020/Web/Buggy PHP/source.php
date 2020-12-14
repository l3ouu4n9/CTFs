<?php
require('req.php');
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
show_source("index.php");
if (empty($_GET['hash']) || empty($_GET['cmd']) || empty($_GET['tmp'])){
    exit;
}

$key = getenv('KEY');

if(isset($_GET['tmp']))
    $key = hash_hmac('sha256',$_GET['tmp'],$key);

$hash = hash_hmac('sha256',$_GET['cmd'],$key);

if ($hash !== $_GET['hash']) {
    echo "NO flag for you";
    exit;
}

$cmd = preg_replace($filter, '', $_GET['cmd']);
echo exec("cmd ".$cmd);
?>