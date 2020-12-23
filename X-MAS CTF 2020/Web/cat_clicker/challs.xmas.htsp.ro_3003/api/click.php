<?php

include('helper.php');

$state = $_POST['state'];
$hash = $_POST['hash'];

if(!isset($state) || !isset($hash) || !verifyState($state, $hash)) {
	echo json_encode(array('success' => false));
	die();
}

$cats = getCatsNo($state);
$cats = $cats + 1;
$parentsLimit = getParentsLimit($state);

if($cats > $parentsLimit) {
	echo json_encode(array('success' => false));
	die();
}

$newState = "$parentsLimit | $cats";
$newHash = hashFor($newState);

echo json_encode(array('state' => $newState, 'hash' => $newHash, 'success' => true));

?>