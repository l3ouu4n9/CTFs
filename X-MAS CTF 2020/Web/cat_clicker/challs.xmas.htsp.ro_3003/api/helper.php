<?php

function hashFor($state) {
	$secret = getenv("SECRET_THINGY"); // 64 random characters - impossible to guess
	$s = "$secret | $state";
	return md5($s);
}


function verifyState($state, $hash) {
	return $hash === hashFor($state);
}


function getCatsNo($state) {
	$arr = explode(" | ", $state);
	return intval(end($arr));
}


function getParentsLimit($state) {
	$arr = explode(" | ", $state);
	return intval(reset($arr));
}

?>