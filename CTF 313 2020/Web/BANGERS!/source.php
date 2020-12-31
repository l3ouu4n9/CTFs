<?php

// Web03 Challenge "Bangers"

include('flag.php');

error_reporting(0);

if(!isset($_GET["taws"])){
    highlight_file(__FILE__);
    die();
}

$taws = $_GET['taws'];
if($taws != md5($taws)){
    die("Your Dead");
}

echo substr($flag,0,15) . "\n";

$tabernacle = $_GET['tabernacle']; 
$quantile = $_GET['quantile']; 


if(!($tabernacle) || !($quantile)){
    die("Death has found you");
}

if ($tabernacle === $quantile) {
    die("There are many ways to die. You seem to find them easily");
}

if (hash('md5', $saltysalt . $tabernacle) == hash('md5', $saltysalt . $quantile)) {
    echo substr($flag, 0, 30) . "\n";
}

class Wutang {
    var $wut;
    var $ang;
}

$gat = $_GET['gat'];

if (!($gat)) {
    die("Bang, you dead");
}

$banger = unserialize($gat);

if ($banger) {

    $banger->ang=$flag;
    if ($banger->ang === $banger->wut) {
        echo $banger->ang ."\n";
    } else {
        die("Death Brought BANGERS");
    }

} else {

    die("Ba-ba-ba BANGERRR. Dead.");
}

?>