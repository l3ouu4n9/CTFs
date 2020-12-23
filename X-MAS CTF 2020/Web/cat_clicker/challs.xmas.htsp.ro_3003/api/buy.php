<?php

include('helper.php');

$state = $_POST['state'];
$hash = $_POST['hash'];
$itemId = $_POST['item_id'];

if(!isset($state) || !isset($hash) || !isset($itemId) || !verifyState($state, $hash, true) || ($itemId !== "1" && $itemId !== "2")) {
	echo json_encode(array('success' => false));
	die();
}

$cats = getCatsNo($state);
$item = "";
$ok = true;

if($itemId === "1") {
	if($cats >= 1) {
		$cats -= 1;
		$item = "FAKE-X-MAS{fake-flag-dont-submit-signed-yakuhito}";
	} else {
		$ok = false;
	}
} else {
	if($cats >= 13) {
		$cats = 1337;
		$item = getenv("FLAG");
	} else {
		$ok = false;
	}
}
$parentsLimit = getParentsLimit($state);
$newState = "$parentsLimit | $cats";
$newHash = hashFor($newState);

if($ok === true) {
	echo json_encode(array('state' => $newState, 'hash' => $newHash, 'success' => $ok, 'item' => $item));
} else {
	echo json_encode(array('success' => false));
}

?>